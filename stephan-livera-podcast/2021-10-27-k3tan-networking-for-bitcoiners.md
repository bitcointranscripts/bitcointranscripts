---
title: Networking For Bitcoiners
transcript_by: Stephan Livera
speakers:
  - K3tan
date: 2021-10-27
media: https://www.youtube.com/watch?v=3NA3ojAgw9Y
---
podcast: https://stephanlivera.com/episode/315/

Stephan Livera:

k3tan, welcome to the show.

K3tan:

Thank you. Thanks for having me.

Stephan Livera:

Mr. Ministry of Nodes and Mr. Calyx and also Pop OS. Obviously I had to get you on the show and it was time to get you on. So for anyone who doesn’t know you, tell us a little bit about yourself.

K3tan:

My name’s k3tan, and I am the co-founder of Ministry of Nodes with you, Stefan, and we provide Bitcoin education material, particularly on YouTube. We also have guides and we do consulting sessions as well. So yeah, that’s just a little bit about me. I’m into open-source software, and obviously a hardcore diehard Bitcoiner.

Stephan Livera:

Yeah. Of course, of course. So for anyone who doesn’t know, K3tan is one of my first friends in Bitcoin. He’s one of the people that I’ve known for a long time. It was an interesting journey bringing k3tan down the the rabbit hole with me. I think it was the white paper that did it for him. Today we were going to talk about [home computer] networking for Bitcoiners, because I think this is some stuff that maybe Bitcoin people, if you’re new, you might not have thought about this. You might not know a lot about it. And this happens to be one of k3tan’s areas that he loves to talk about. He loves to read and research about it. So this is the perfect thing for him to help educate our Bitcoin community about it. So maybe you want to just start with some of the basics. Why should we even care about networking? Why do we even care about our home network? Don’t I just like turn on and the wifi works?

K3tan:

Yeah. Look, I think we should start caring as Bitcoiners about our home networks from a security and privacy perspective. The reason is, is before Bitcoin was invented, most hackers and most crackers would be looking at things like governments—would be looking at places that hold identity information, corporations, banks, financial institutions, exchanges, those sorts of things, right? That’s where you get the most bang for buck. Now with the invention of Bitcoin, however, that game slightly changes in that now, home networks could potentially be something of worth. I’m not specifically talking about cold storage, I think cold storage and hardware wallets are fantastic devices and tools. And I think you and I both agree on that. But I’m talking more about hot wallets. And in the context of specifically Lightning Network as well as CoinJoin, these are two predominant hot wallets that I am seeing that are now becoming more and more popular and becoming online. So if you’ve got devices that are able to talk to each other on a network, we want to make sure what those devices are and make sure that we can exclude certain devices and those sorts of things. And this is where your home network will need to be at least somewhat secure to prevent something going wrong with your Lightning Network node or your CoinJoined wallet. I can totally foresee a scenario where someone gets into your wifi, your poorly passworded wifi logs in to your MyNode, logs in to your Ride the Lightning, and then basically closes all the channels, sweeps all the funds and does it between the hours of twelve o’clock at night and four o’clock in the morning whilst you’re asleep. I can totally see that happening. So this is why we need to start to look into and improve and upgrade our networks because some of these routers have been around for a very, very long time. This is why I think we should start caring about our home networks.

Stephan Livera:

Right. That’s the security part which you’ve outlined very nicely for listeners, but it’s also the usability aspects of it: that, when you’re learning how to use Bitcoin, you have to think about, Well, how do I use it? And how do I, for example, have a wallet on my phone and connect that back to my home node? Well, you might need to know a little bit of networking in order to achieve that. So that’s also a usability and accessibility aspect because you might not be inside your home at the time and outside of wifi range. How do you connect back? What’s involved with that? So when we’re talking basics of networking, what are some of the key high-level things that every Bitcoiner should know?

K3tan:

Okay. I’ve got a couple of tips for you. The first one is: if you haven’t logged into your router, I would strongly suggest that you do so. You’ll probably find that these routers will have a very insecure default username and password, and that will be assigned to you or given to you by your internet service provider. Now on the back of them, they might have an address that you can go to. It’ll be something like HTTP://192.168.1.1. And then you enter in a username and password, and it presents you with the router login. I would strongly suggest looking and seeing what functions are available, if you haven’t already. The next thing that I would also recommend is changing that default password. Say, for example, you came in, Stephan, to my place and I said, Hey, here’s the wifi password. And then you went into 192.168.1.1 and it had the default username and password. Well, you’re now messing with my network and I don’t particularly want that. So what I would recommend is changing that password to something a little bit more secure, but not only changing the password to access the router itself, but also to change your wifi password. That is something that I think that all Bitcoiners should be looking at because that is an attack surface. The thing that you should change it to—and this is just a recommendation only—is at least you should be using WPA2. A lot of these old-school routers will be using just normal WPA, which is now obsolete. But you want to be doing WPA2 as the password encryption methodology. And also you want to be using a strong password. And the way that I like to do it is: if you go onto the Electronic Frontier Foundation [eff.org], there is a way that you can use some dice. If you roll some dice, it’s got a word list and it corresponds with your dice roll. And so if you add, say, five words put together randomly, you get a very, very good secure password that you can speak to in case you need it to give to somebody, but it’s accessible to everybody as well. And it is secure. So that’s another tip for you. One more tip that I would also give is: using guest wifis. Your router in there will have the ability to segregate networks. So you might have a trusted network and a guest network. That guest network can host things like your televisions, your Chromecast, security cameras, internet of thingd devices, work laptops—now that we’re working from home more and more. If you don’t want your work laptop on your trusted network, then you might want to put that onto your guest network as well. So these are some of the things that you can do. Also, keep your router up to date, to the latest firmware that is provided by the router manufacturer. So those four tips, I think, are the baseline of home networks.

Stephan Livera:

Yeah. And so there’s a bunch of things in there you were saying around fixing up your login because it’s typically “admin password” or something very basic like that. And so anyone who has that—what kinds of [malicious] things could they do to you if they knew that?

K3tan:

Oh boy. Well, they could start to shut you out of your own network, that’s one thing—all of your devices, your Internet stops working. They can then see which addresses have your node. They can see all the devices on your network. They can snoop traffic. So if you’re using un-encrypted ways of logging into websites and using your username and passwords, they can snoop through there. They can pretty much spy on you using advanced tools that are available on the market there. So it’s probably worthwhile not having devices that you don’t trust on your network. Basically, keeping your network to the devices that you actually know. I am sure: you will be surprised when you log in to your router page and you look at the device list that’s available to you, you will see a lot of devices there. I’ve seen homes with a lot of devices and they don’t know what they are. This can present a risk.

Stephan Livera:

Right. In some cases that could have been some guest who came over earlier and it was their iPhone, or their phone or their tablet or whatever. And then they went away. In some cases, it might be that. But in other cases it could be malicious. There could be somebody who was doing what’s called WiFi wardriving, right?

K3tan:

Yeah. That’s right. So what you could do is screen through all of the devices. So when you reset your WiFi password and you reset your entire router—at that point, that is a good time to go, Okay, these are the devices that I’m expecting to be on the network and on the guest network, and these are the devices that are meant to be on the trusted network. So that’s a really good time to do that. You’ll lose Internet connectivity for a couple of minutes, but I think it’s a worthwhile exercise to just bring everything back online so you know the devices that are being connected onto your network.

Stephan Livera:

So don’t worry guys, you can quickly catch back up to the chain tip. You’ll be all right. It’s only a few minutes, you Bitcoin nodes out there. So with the guest network and the segregation between that and your trusted network, how does that work? And how does the segregation work there?

K3tan:

Yeah. So in your router page, common route—like I’m talking more advanced routers, but even just common routers—will now have the ability to tick a function where you can enable “guest WiFi,” and that will have its own WiFi password. It will broadcast its own WiFi name. So you might have a WiFi name and then WiFi name dash guest. And that guest would be where you would connect through. What happens is: in the guest network, no devices are allowed to speak to each other. So you can’t access your Bitcoin node from the guest WiFi. You won’t be able to access any other devices. The only thing it’s got is Internet connection, which is what is required to do, for example, your television or your Chromecast. That is all that’s required. There’s no ability to look at other devices on the network. And that’s the strength of a guest WiFi.

Stephan Livera:

I see. Yeah. You mentioned updating the browser to the latest version. Why is that important? Is it mostly bug fixes, patching, and vulnerabilities?

K3tan:

Yeah, that’s exactly right. So if you keep your router up to date, you should be able to—obviously these companies like Netgear and D-Link and Linksys and all these guys who provide routers for internet service providers, they keep their routers’ firmware up to date for any of the latest vulnerabilities and bug fixes and all those sorts of things. So what you want to do is periodically have a look at your router manufacturer and keep that router up to date such that you obtain the benefits of those security updates.

Stephan Livera:

And so that normally is the process that you would do inside your 192.168.1.1 web interface, as opposed to having to do a physical upgrade process?

K3tan:

That’s right. So you do that all in your router login. All of the tips [I’m talking about] are within the router login page that is made available to you on the page there.

Stephan Livera:

Gotcha. And so maybe if you could give us a quick overview, like how do routers work and how do they—like, for an example, you might see this DHCP dynamic IP, how does a router assign IPs out to the users on that network?

K3tan:

Okay. So your internet service provider assigns you a public IP address. Now you can get a static public-facing IP address, or you can get a dynamic public-facing IP address. A dynamic one—as the name suggests—keeps changing over and over again. And it constantly changes. Whereas the static one stays the same. Some internet service providers will not provide you with a public-facing IP address. For example, if you’re on a mobile wireless network, that won’t have a public-facing IP address. Now, that modem will then connect through to your router. And your router is basically the first device in your home that will be connected to the internet. And it will be assigned the IP address, or what’s known as a WAN IP address—a wide area network IP address. Now, that is separate and distinct from your local IP address—your LAN IP address. So you’ve got a local area network and a wide area network. Your wide area network is basically going out to the rest of the world and fetching information. And your local IP addresses are just being assigned—basically we can’t have every single device having a wide area network IP address. What is happening here is that your local IP addresses are sharing that one WAN IP. And so everything is traversed through this WAN IP address. That is distinct to you. Your internet service provider—because you’ve paid for it—they know your address, they know your credit card details, they know exactly what internet connection is looking up what. And in countries like Australia, internet service providers are required to keep “metadata”—which they define very loose—on Internet connections for up to two years. So they do this through what’s known as a domain name server. When you go out and you request information on the Internet, the domain name server will say, Okay, this is, say for example you want it to go to google.com. This is google.com’s IP address and it puts you in touch with that IP address—or it converts it. So that is how you’re creating these logs. Internal to your network, though, your router is what’s going to assign IP addresses, or internal IP addresses. So your router login is 192.168.1.1. And then say, for example, you bring on your mobile phone onto the WiFi. It will have 192.168.1.2, and then .3, .4, .5. And the service that is doing this is called a DHCP server. That is run on your router.

Stephan Livera:

Gotcha. So that’s the big connection there. So I think you were touching on this before as well, but what’s the importance then of hiding your IP? Or what are the privacy considerations around what your—now in this case—your WAN IP is?

K3tan:

Yeah. So as I was alluding to, what you want to do is try to make sure that your WAN IP address is not something that is—you want to hide it because this is the gateway into your home network. It’s the door that people knock that will basically allow them access into your home network. And so the job of the router, which is very, very important, is to act as almost like a firewall between your devices at home and the public information highway that people are trying to look into. The privacy considerations are basically: you want to have as minimal attack surface as possible. So that’s why you never give away your public IP address. And it’s also being logged. So logs of that IP address going to, say for example the Sydney Morning Herald website, are being generated via the DNS server, but also from Sydney Morning Herald’s end. Their server would be logging which IP is accessing what websites as well. So you’re leaking a lot of information when you browse the Internet. And so you want to try and protect that as best as you can.

Stephan Livera:

I see. So in practice that will be difficult for most people to achieve, but it is worthwhile thinking about it in that it essentially doxxes whoever is paying the bill for your ISP, which, if you’re paying the bill for that ISP, well then that ISP knows your credit card details or your direct debit bank, whatever. And that can be tied back to you. So if you are out doing something on the Internet and that can be tied back to your identity, then that can be a concern for people out there. And tying back to the point you were saying earlier about securing your router, just in the same way that for example, there were people who were illegally buying a KYC credential to get a Binance account or whatever—they’re using someone else’s KYC, right? So in the same way, if somebody hacks your WiFi and then uses it to do illegal things, it might look like you’re the one doing the illegal thing. So that’s also another thing to think about. And then of course, depending on how private you want to be with your use of Bitcoin, there may be people in countries around the world where they do not want to disclose that they are even using Bitcoin. So that’s probably an aspect to think about there. So then bringing it to networking for Bitcoiners. Let’s talk a little bit more about what it looks like if you want to use your Bitcoin node on your local home networks. So maybe as an example, you’ve got MyNode or Umbrel, or one of these different node packages, or you’ve got your own box and it’s whatever that IP number [is]. What does it look like if you want to hook up our own Bitcoin wallets with that node internally?

K3tan:

So in reality, you’ve got two options for yourself. You can do what’s known as a VPN, so you can tunnel in. Or you can go over TOR. Now each of them have their own pros and cons which I’ll go through, but basically with the VPN, there is some high level of configurability there, but it is quick and it’s accessible, it’s reliable. It’s very, very good. Whereas TOR is very, very easy to configure, but it can’t have reliability and it’s a little bit slower. So those are the two trade-offs here. Now, my preference is I like to use VPNs. Now, what I do is I have a VPN on my router, or what’s known as a VPN server. And a lot of people confuse the two: there’s VPN clients, and [then] VPN server. And VPN servers allow you to connect back to your home network whilst you’re out and about, and access the services that are in your home. For example, your Bitcoin node. So you might have an Electrum server there, or you might have your Lightning Network node. You can actually hook up your phone to your Lightning Network node via a VPN server. And so you can host it on your router or you can host it internally onto your network as well, but then you would need to open up a port on your router to allow that traffic in. And obviously it’s encrypted and it’s got username and passwords and those sorts of things as well to prevent other people from accessing it from the worldwide web as well. So that’s one way. Or the minor packages and various other packages will also broadcast an onion address for TOR. And so in your mobile app, you can then say, Alright, well, can you connect to this onion address? And that will then give your Lightning Network your funds, and you can use Zeus wallet or Zap wallet to do that. So those are the two ways of doing it, separate and distinct from a VPN client, which is where you are basically trying to hide your IP address. And that is connecting through to something like either Mullvad VPN or Proton VPN or IVPN or something like that. That’s different compared to the VPN server that we’re talking about when it comes to accessing our Bitcoin node from an external network.

Stephan Livera:

Gotcha. Yeah. So the typical examples, let’s say you are running Ronin Dojo, and then that automatically does TOR and it’s doing a TOR hidden service. And then while you’re out and about you pull out your Samourai wallet and previously you would have “paired it” with your own Ronin Dojo, which is your own Samourai wallet server. And then that’s using the TOR network to find itself back home, or find the answers to how many transactions I’ve done, and what’s my balance, and what are my addresses and all of that. And then, as you were saying, the other way is to do via VPN. So I think in practice, it seems like if people just want an easy way to do this, probably something like Sparrow wallet on their laptop connecting back to their own Electrs—Electrum rust server—which is running on their home node, which might be on the various different node implementations, Raspiblitz, Ronin Dojo, Nodl, MyNode, Umbrel, et cetera. You would have an onion address to connect to which you would—basically, usually inside your node, you’d have a copy paste panel and you would copy that address, and you would then paste that into, let’s say, Sparrow wallet as an example, right?

K3tan:

That’s exactly right. And then Sparrow wallet will then traverse through the Tor network and then connect to your Electrum server and then fetch you all of your balances, right from your home, and the Bitcoin node that is running at home. So that’s exactly how you would do that when you’re out and about on your laptop or even on your mobile phone as well.

Stephan Livera:

And so that might be an example. So let’s say a listener is thinking about doing self-sovereign multisig and they want to roll their own. Well, they could be running their own node back home and have the multisig keys out in different locations and bring the laptop. As long as the laptop has Internet connection, then you could basically use that mechanism to do your own keys and your own node as well. So that’s an important aspect because people who are new, they might not understand that difference between holding your own keys versus running your own node. So there are different aspects of it that sometimes can be rolled together in one sense. And then the other part as well is just, let’s just say you’re in your home now, you’re at home, you’re on your own PC desktop, and you just want to connect to your node just literally three meters away from you. How does that work? Do you just use the local area network IP or what’s that?

K3tan:

That’s right. So if you’re within the home network and it’s not an issue to go out and you just own a desktop or something, then what you could do is just use your local area network. So for example, in your router, your router page will have all the devices and their IP addresses. So your Raspiblitz might have 192.168.13, for instance. And what you would do is on your desktop, you’d open up Sparrow wallet and you would connect to the Electrum server at 192.168.13. And the specific port for Electrs is I think 50002 or 50001. So that’s how you would do it. You just use your local area network. And that’s the easiest way of doing it. But I think now with people wanting to be out and about more, and wanting to access their nodes, they’ll probably need to either use TOR or a VPN server to be able to tunnel back in.

Stephan Livera:

Right. So what we’re talking about is at a conceptual level what’s going on. Now in practice, what might happen over time is more and more of the products and services out there—the ideally FOSS stuff—will build it in a way that’s easy that you don’t have to worry about it, it’s going in the background. So one example would be, I know the Ronin Dojo guys are looking at this of having your node back at home, your Rasberry Pi [inaudible] node, running at home, and it’s running the TOR service and actually that’s accessible just on the TOR browser. So even if you’re out, as an example, you might be on your laptop with TOR and you just type in this TOR address and boom, now you can keep an eye on your mixes or what’s going on in terms of your CoinJoin.

K3tan:

Yeah. That that’s another option as well when you’re out and about to just have everything on the Tor browser. I think that that’s probably a good idea as well, where people can look and manage all of their Bitcoin-related activities on the fly over the TOR browser. I think that that’s a fantastic tool. Another thing that’s making it easier: there’s two pieces of open-source software that are making networking easier from a VPN perspective as well, is ZeroTier and Tailscale. Now ZeroTier is using OpenVPN as the protocol. And you basically install this piece of software on your computers or on your devices, and when you connect to the VPN there, it will allow you to access your various devices no matter where those devices are in the world. And Tailscale is doing the same thing, but they’re using the the newer WireGuard protocol. And so keep an eye on those projects as well, because that makes it easier for Bitcoiners to be able to—say for example, you wanted to host your node at your parents’ place and you want to connect back to that one. Well, you can have multiple devices at multiple locations and all sync that up using ZeroTier and Tailscale as an option there. So that’s something that’s coming down the pipeline to make these networking things easier for Bitcoiners.

Stephan Livera:

I see. Yeah. And it is fair to say that some of these things can be a little bit slower if you’re trying to do it all over TOR, or it might be a bit less reliable or there might be times where you are out and you’re trying to call back and check your balances on your Samourai wallet and sometimes it just might be a little bit slow. And sometimes you just have to retry it and just check. And again, part of that is like the software is getting better at managing that as well, but it is just something to think about. And yeah, in fairness to the different node packages, a lot of them are now trying to do that also. So I know the Start9 Embassy has also a TOR back to your own Embassy. I think Umbrel has it and I think MyNode has it. They probably all have it. But it’s basically a web interface back to your node as opposed to like literally the wallet interface back to your own node.

K3tan:

Right. So these are all improvements that we’re starting to see because we’re seeing that—like if you look at the Telegram support channels, it is flooded with How do I do this over TOR, or How do I do this over VPN? It’s getting very, very confusing, and I’m liking the fact that these node packages are making it easier for people to hook back to your own node over TOR or over VPN. And I think the Umbrel guys are certainly looking into Tailscale as well, I know that. It’s constantly improving. It’s getting better for Bitcoiners who want to be self-sovereign. And yeah, we’re using the tools to be able to do that.

Stephan Livera:

And just on an Uncle Jim note, calling back to our good friend, Matt Odell: while we’re here, it’s a good point to mention that this is also a good tool if you are trying to Uncle Jim for somebody else. So let’s say you’ve got a newcoiner friend, and you’re like, Hey man, download Sparrow wallet. And when it gives you that thing to go into the configuration in the server and here, paste in this string—and done! Now, you’re their Uncle Jim.

K3tan:

That’s exactly right. So you can see now that you can scale your Bitcoin node to help others. And that’s what this whole movement is about is just really making sure that we are protecting each other and making sure that we are helping other newcomers into the space and not make the same mistakes that we unfortunately made. And so when you have a trusted party, like a friend that you can rely on, whilst they’re learning to be more self-sovereign, you can put them temporarily on your node or your Dojo or your Electrum server, or your LND hub, and you can then help them and teach them, give them the wow factor of Bitcoin, and then teach them the self-sovereign way of how you do it. And then they can hopefully help their friends and family and so forth. And so this sort of virus spreads.

Stephan Livera:

Yeah. Also another interesting element: calling back to the security part you were mentioning earlier—and this reminds me of the point that Craig Raw of Sparrow Wallet was making around, if you are using Bitcoin Core directly, in order for your computer to be able to know how many coins you have, it has to keep your public keys in plain text, or it has to exist on that node—and so that might also be a privacy and security concern if somebody gets access to your network. Because at that point they could try to figure out, Oh, let me see what’s on k3tan’s box. Oh, here’s his Bitcoin Core. Oh, wait, here are the public keys for his coins. Boom. Now I know how many coins you have.

K3tan:

Yeah, that’s exactly right. So if you do have devices that are on your network and they have access to a Bitcoin node, the first thing that they’re going to do is go into the wallets folder and see what’s in there. And the wallets folder will have public key addresses, unfortunately. And those public key addresses could then be used to then see—because it’s a public ledger—and you can see how much the wallet contains. That could be a privacy issue for you later on in the track.

Stephan Livera:

Right. And of course these are all trade-offs, right? So you might still think it’s worthwhile to do it that way because you need to—you need to do something. But one mitigation that the Sparrow wallet team essentially is making, is this idea that you should preferentially use an Electrum server, because especially if the remote user is connecting through TOR, then you don’t have an IP address to tie it back to. So it would just feed out, Oh, here’s your balances, Electrum client, from my Electrum server, but I don’t know who you are.

K3tan:

That’s exactly right. And that’s one of the great things about an Electrum server. It allows people to utilize or fetch their balances very, very quickly, but use multiple xpubs to keep querying that without creating logs, that show which xpubs are being used, or being asked for or requested. So that’s really, really handy. And yeah, that’s why an Electrum server is probably the more preferential method of doing it rather than importing your wallet into Bitcoin Core.

Stephan Livera:

Okay. And also just on this use of VPNs, this is another thing I’ve seen where—and this ties into VPN clients and servers a little bit—but also this concept of whether you just use a laptop or a desktop software client to connect to Mullvad, for example, versus trying to set up your VPN at the router level, such that all traffic through your whole network is going through the VPN. Can you tell us a little bit about that? Like what’s the difference there?

K3tan:

Yes. So essentially what’s happening here is that if you connect your PC to say, for example, Mullvad VPN, that PC is being protected and all the traffic that is coming in and out of that of that PC is behind a shared IP address, not the IP address of your internet service provider IP address. That gives you some level of privacy, and it reduced the logs that are being associated with your public IP address assigned to you by your internet service provider. So that is just for that device though. Now sometimes what happens is that Mullvad will only allow you up to five devices. So you might have your laptop, you might have your desktop, you might have your mobile phone, and you might have a friend who wants to use it, or you might have another device and it quickly becomes, Okay, I’ve only got five connections that are able to be concurrent at the one time. So at the router level, though, if you connect it at—and some routers allow this functionality—if you connect it through on your router, every single device on your network will funnel all the traffic through the VPN and therefore protect your privacy from your internet service provider and other websites who are logging this information. So that is a better way of going about it. That’s how I do it. You can use open source tools to be able to do this. But yeah, you can use that functionality in your router to be able to do that. That’s something that listeners might want to consider as well.

Stephan Livera:

Yeah. Right. And so in some cases it may be that your computer-level use of a VPN—so say Mullvad just on my laptop—it might still leak some of the traffic out through the normal clearnet internet. And maybe that’s also another angle there, that if you do it at the router level, it’s maybe a little bit more well-covered.

K3tan:

That’s right. So say for example, you’ve got a Raspberry Pi there, trying to put a VPN on a Raspberry Pi—it’s possible, but if you do it at the router level, then you don’t need to do it for any device that you connect onto your network. And so therefore all of the traffic that you’ve generated throughout your entire Internet history is then protected by a VPN. And you’re not subject to these laws where you’ve got your two years worth of metadata being collected because you’re not using your internet service providers’ DNS, you’re using Mullvad’s DNS.

Stephan Livera:

Now let’s talk about this question of running a home box node versus a VPS. So VPS stands for virtual private server. And as an example, you might be running BTCPay on LunaNode, and they’ve got a very easy LunaNode web deploy process. So that’s one example of a VPS service that you might be using for your Bitcoin stuff. But the alternative is to try and run it literally bare metal in your own home. So can you explain some of the different considerations here?

K3tan:

Yeah. So look, if you’re using a VPS, obviously you are at the subject of your VPS provider. That is a trusted third party that you are relying upon. And they have the ability, if they so wish, they can shut that down at any at a moment’s notice. So that is a trade-off that you are making. And it also costs money so it’s usually something nominal like $5 a month or $10 a month or whatever it is. But they have the ability to shut you down. They can also take a look at your traffic potentially and see what you’re doing. And that is what a VPS offers. But reliability and uptime—I don’t think you’re ever going to have a problem with a VPS. Like, that is their bread and butter. That is going to be something that you can rely upon, particularly if you’re a digital nomad type of person and you don’t have that ability to host something at home. If you’re constantly out and about and you don’t have a permanent address, well then VPS is probably the fit for you. You must rely on somebody else to be able to do that, because you can’t just keep taking your Raspberry Pi offline all the time to your next hotel location or to your next location—it just doesn’t make sense. As compared to a home box where you can build everything up yourself and run your BTCPay server, expose it out to the world, and you’re able to host things yourself. However, that being said, there’s reliability. So say for example, the electricity goes or the Internet goes at your place. Well, now you don’t have a BTCPay server anymore. So those are the trade-offs there. Whilst it’s free, it also comes with a bit of a trade-off to that extent as well. But if you are in a permanent address, then that might mean something—you know, it’s the more self-sovereign way and you can’t be shut down. Those are the trade-offs there.

Stephan Livera:

And also arguably there is a trade-off there around exposing your home IP. So if you want to run a Bitcoin store, receive payment for your products or services you’re selling online, that’s also something that you do have to think about. Because again, as we were saying earlier, you’re doxxing the IP, you’re doxing the address and the name of the person who paid for that ISP, basically.

K3tan:

That’s exactly right. So if you are running something like that from your home, you are potentially doxxing your IP. There are ways to hide that. But then again, it’s trusted third parties once again, who you would need to then trust. There is no perfect solution, unfortunately. The Internet, when it [was] first made, it just wasn’t by default private. And so these are some of the trade-offs that happen when you’re using a VPS versus doing it yourself in your own home. Yes, you are doxxing your own IP address, but there are mitigating factors if you are willing to trust somebody else with that information. It’s really up to you.

Stephan Livera:

Gotcha. Yeah. And then while we’re here, Bitcoiners tend to have more of a focus around self-sovereignty. So you might be interested to run other services on this kind of box, as an example, your own password manager, a Bitwarden, or your Nextcloud, which is like your own version of your own home-rolled, open source Microsoft office kind of thing, Matrix, your chat server, or Mastodon, your own decentralized, distributed social media. Can you tell us a little bit about what other things to think about there?

K3tan:

Yeah. So look, I’ve been going down the rabbit hole of self-hosting for quite some time now, and I love it. So what you can do is you can host your own services, so you don’t need to rely on trusted third parties. So for example, if you don’t want to use Bitwarden server, you can create your own Bitwarden server because it is open source software. And so instead of calling out to a bitwarden.com, you call out to your own network and retrieve your passwords from your own home network. Same thing with Mastodon. It is a Twitter alternative, but basically it’s self-hosted. And one of the advantages is that the censorship and the de-platforming and those sorts of things can’t occur. That’s not to say that nobody can block you. Yeah, you can be blocked still, but your words then still remain there up for everybody to see if they so wish to listen. So that’s another example. And then you’ve also got Nextcloud, which as you mentioned, is a great open source Dropbox-style alternative that you can host and manage your data through that. These are all things that you can do. I would strongly recommend that you keep your node separate if you are doing these sorts of other peripheral things self-hosting. But I know that the Umbrel guys and the Start9 guys, they are doing it all in the Raspberry Pi. I’m interested to see how that works out long-term and seeing what happens with that. But at this point, my conscience is telling me, Hey, Bitcoin-related activities, one piece of device, and self-hosting activities aother piece of device, depending upon your circumstances. But that’s just me personally. Let’s see what happens in that space.

Stephan Livera:

And I suppose the Start9 Labs person could come back and say, Well fine, k3tan, what I might do is have two: I’d have one for my Bitcoin stuff and one for the non-Bitcoin stuff.

K3tan:

That’s exactly right. Yeah. So that just segregates out the resources, particularly in high-resource environments. Sometimes when—I know now that the Electrum server has upgraded, and now you need to re-index all of the transactions, the 420 gigabytes. That’s going to take some time on a Raspberry Pi. And then to have that slowing everything down, like, for example, a Nextcloud as well, during that time what’s going to happen there? That’s the key concerns that I’ve got there. But you know, let’s see what happens. You might want to segregate and have two Raspberry Pis, one running Bitcoin-only, and one running all of your other peripheral services as well. That’s a great solution.

Stephan Livera:

And while we’re talking about all the upsides of self-sovereignty, I think we should probably also, to be fair, talk about some of the downsides, right? Because there can be issues with these things, and it’s probably good to give a fair presentation of what that is. So yes, the upside is: look, you’re being more self-sovereign, you’re not as reliant on trusted third parties or other service providers. What are some of the downsides that you have seen in trying to go down this pathway?

K3tan:

Okay. So the electricity shuts down at home. That is a downside, right? If the electricity goes out or your internet service provider goes out for some strange reason, it is just painful. You won’t be able to tunnel back. You could be out and about somewhere else and at home, no one’s home, no one can look into it and you’re just left high and dry. It’s not helpful. It’s also—there’s time involved. There’s your time in being able to set this up, make it robust, understand what’s going on. There is a bit of knowledge, there is a bit of a journey—call it a rabbit hole—that you might need to go down to be able to familiarize yourself with some of the concepts and the terms that are going on. So those are some of the downsides obviously, and it can be finicky. It can take a little bit of time. It’s going to, but I think once you’re familiar with what’s going on, it can become easier over time, but that’s the trade-off, is your time.

Stephan Livera:

Yeah. So I think it’s probably fair to say it will require a bit more technical competence and it will require a bit more time in troubleshooting things when go wrong. You might just need to be able to learn how to stop and restart a service or to restart the box. And you might need to be comfortable with using SSH while you’re out to SSH back into your home box, to do these things. And that will take you time. And there might be connectivity issues there and all sorts of things. But these are some of the things just to give a fair presentation of it.

K3tan:

I agree. Totally. Self-sovereignty is sometimes not for everybody. And this is where trusted providers in the space can offer solutions for those people who are just starting off their journey, or just want to just jump straight into a level of service that they can recommend or that they can stick to for now and then learn the ropes and then maybe transition away from them. It’s up to you what you want to do and what you want to decide to do. But yeah, there is a level of competency that is required. That is a fair, fair point, Stephan.

Stephan Livera:

And also, I mean, this is maybe not as networking related, but just generally want to get your thoughts on the use of Raspberry Pi devices versus say a proper box, or maybe somewhere in between, like people who use like ROCKPro64 and things like that. I know you’ve got thoughts on this.

K3tan:

Yeah, look, I hope I don’t get canceled for this, but I am not a fan of the Raspberry Pis today. Look, I think that they are great learning materials. They are good for Hackerman type scenarios where you’re just entry-level if you want to play around with things, if you want to test environments, if you want to do those sorts of things. But a production environment, I believe, requires a little bit more grunt, a little bit more overhead. For example, I know guys who have started with their Lightning Network nodes and those channels have now increased. The RAM usage has increased. They’re going to upgrade to the latest version of Electrum. The resources and the systems are going to increase. And I suspect that these changes will keep coming through as time progresses. And so if we are limiting to a small board computer then that can present some channel challenges. Whereas if you get older hardware that has a little bit more grunt and may be a little bit more expensive—I’m not talking thousands, I’m still talking hundreds of dollars—then maybe that could present a better deal for those who require that reliability or that grunt. Whereas a Raspberry Pi is a great mechanism for learning to understand what’s going on. And then moving over to a node box for a more production environment, I think, is probably a better investment of the resources that you’re going to deploy. Specifically if you’re running routing channels and those sorts of type of activities, you want something that’s not going to be flimsy that when you the upgrade button that it is actually going to upgrade and there’s no technical glitches that are going to happen. These things just come with time, I guess. And I’m sure the other implementations are going to improve over time, but these are some of the things that I think Bitcoiners are facing, and I think they need a strong, reliable method. And I’ve got a whole YouTube series called the Ubuntu NodeBox guide, it’s on YouTube at youtube.com/ministryofnodes. It’s an entire playlist to take you through some of the commands and what’s happening in the background, if listeners would like to learn. Run it at 2x speed to save some time, and you might be able to get up to speed on what services are actually being run on your MyNode or your Dojo or your Ronin Dojo or whatever. And you can then see how it works in the backend through my video tutorials. So open arms, please. Don’t hate on me too much for my opinions.

Stephan Livera:

And it’s probably fair to say that it depends how many services you want to run on that Raspberry Pi, like I think one thing that maybe a newcoiner or a relatively new Bitcoin pleb is coming in, it’s like, Yeah, I want to run my node. And now I’ve seen everyone Tweet out their pictures of their node. I want to do it too. But what might happen is you might be in a situation where at the start, it’s all working fine, but then as you start adding more and more services and as time runs on, you find the reliability starts to become more of a concern. Is that something you’ve seen or do you have any comments to add there?

K3tan:

Yeah, look, I think a lot of people have come up to me and said, Hey, look, I’m having problems with my Raspberry Pi device. I don’t know if the fan is out or I don’t know if I’m calling this properly or the USB cable is a little bit flimsy and it’s not reading the SSD correctly. There are an array of [difficulties]. There could be power supply issues as well. Like it’s just not having enough power being drawn out of that Raspberry Pi to upgrade things. And so these reliability concerns over time are presenting themselves. Now the really tragic thing is if you’ve got lots of Lightning channels, you’ve deployed some capital on there. And for some strange reason, your Raspberry Pi has some somehow blown up and you now need to recover the channel backups and all that sort of stuff. It’s just painful. And I think Umbrel is providing some good solutions for that, and they’ve recognized that that is an issue. And so they’re providing solutions for backups and those sorts of things as well. So, you know, this space is constantly evolving and it is improving. It’s just, what do we do between now and [inaudible]. And so yeah, these are the things that are just teething issues that are happening.

Stephan Livera:

Yeah. And also it’s fair to say right now, it seems there’s a shortage of Raspberry Pi just globally. So it might be time maybe for some people who want to use ROCKPro64 instead or just upgrade to having a cheap node box. So maybe if you could just outline what are the costs if you were to try to step it up to a node box? What are some of the pieces, the parts, at least in Australian dollar terms or US dollar terms?

K3tan:

We have a website called ozbargain.com that I do. It’s got a lot of deals particularly around computers as well, but you can get these Office X lease refurbished computers that are really, really rock solid, and you can get them, pick them up with 8 gigabytes of RAM, a small SSD which you can then replace with another like a one terabyte SSD, which is what you’re gonna need for a blockchain. But basically we’re looking at about $190 to $200 AUD for a box that has i5 processor and 8 gigabytes of RAM. And chuck in say, $150 for a one terabyte SSD. And you’re looking at somewhere in the vicinity of $350 to $400 for a pretty decent node box that you can run that sits away. Now, I’ve been running mine flawlessly with all the Bitcoiner software available. I’ve run JoinMarket, I’ve run Whirlpool, I’ve run Dojo, I’ve run BTCPay Server, LN bits, LN—all the goodies that the developers are making and it’s been running rock solid for about 3 years straight. I’ve never had a problem with it. And that type of reliability and that type of peace of mind is something that I value, particularly when it comes to the Lightning Network as well. So those are some of the costs that we’re looking at there.

Stephan Livera:

And it’s also important to note, you’re not necessarily going to keep all the keys to your Bitcoin on there. Right now, Lightning and CoinJoin, obviously the keys must remain hot. Those are the common examples. But for your cold storage, you might have that on your ColdCard or your multisig and using Sparrow or Electrum server or Specter desktop, and calling back to the node. So the node does not have the keys for your HODL stack, your big stash. It’s just got a smaller amount which is your CoinJoin or Lightning stuff. Just an important point.

K3tan:

That is an important point, yes. There’s a distinction there between cold storage as well as wallets that are hot. And cold storage, it’s a good distinction there to say that your cold storage will be safe and that it’s only just calling upon the node to retrieve the updated balance information. And you only really need to bring out your ColdCard when you want to sign for a transaction. And that is all air-gapped as well. So there is no Internet connectivity happening there. So it’s pretty rock solid.

Stephan Livera:

Yeah. So I think those are probably the key points. I think that was a really good overview for Bitcoin people who are trying to learn a little bit more. In some ways you do have to become a little bit of a Jack-of-all-trades and learn a little bit about economics and learn a little bit about computers and learn a little bit about markets and finance, and obviously learn a little bit about networking. And that’s just part of becoming a well-rounded Bitcoiner and knowing what it takes. So as we finish off, k3tan, any final tips for the listeners? And of course, where can people find you online?

K3tan:

Yeah look, the tip is to get started. Don’t be too complacent about this. Don’t just say, Oh, you know what, I’ll leave it. I’ll leave my network just with a default username and password. Proactively try to—even if it’s a small steps—to get you started. I think that those are worthwhile endeavors to take. Where you can find me, I’m at @_k3tan on Twitter. You can always find me at Ministry of Nodes as well. And our YouTube channel is at youtube.com/ministryofnodes and our website, ministryofnodes.com.au. If you need any further consulting, I’ve got a calendar there for people to just book in and they can give me a buzz and we can discuss any of the important Bitcoiner topics that you want to have a look through.

Stephan Livera:

Fantastic. Thanks, k3tan!

K3tan:

No worries. Take care, Stephan.

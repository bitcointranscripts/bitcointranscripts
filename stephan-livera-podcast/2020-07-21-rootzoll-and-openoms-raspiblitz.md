---
title: RaspiBlitz
transcript_by: Stephan Livera
speakers:
  - Rootzoll
  - Openoms
date: 2020-07-21
media: https://www.youtube.com/watch?v=2GgabBbEYo0
---
podcast: https://stephanlivera.com/episode/194/

Stephan Livera:

Hi, everyone. Welcome to the Stephan Livera podcast, a show about Bitcoin and Austrian economics today. My guests are Rootzoll and Openoms of the RaspiBlitz project. And if you’re interested in setting up your own Bitcoin node and running lightning and using Coinjoins with JoinMarket and so on, this is a great project to check out. So I’m really looking forward to my discussion with the guys today. Alright. So I’m just bringing in my guests now. Rootzoll and Openoms. Welcome to the show.

Rootzoll:

Hi there.

Openoms:

Hello.

Stephan Livera:

Hey guys. So look I know a little bit about you, but do you want to just take a minute and tell a bit about yourselves to the listeners?

Rootzoll:

Yeah, sure. So I have a background as a computer programmer studied that. After my studies, I was always a little bit curious, like, okay, now studying is over, it was great. I will work for money, so I was always interested. What is this money? So, so it was always a question. And then later I discovered Bitcoin and it put me deeper on that, on that mission. I had a history of like a US startup once, so like 10 years ago. So I saw a little bit from that perspective, then worked in open source, open education software, and then catch up with the room 77 Berlin crowd. So that’s a little bit where we located or at least where I’m located. And from there, like we got deeper into, into Bitcoin of course. And then lightning came up and and kind of Jeff from Fulmo was asking me a bit, like, do you like to go deeper on this? And so we started to organize the lightning hack days. So I’m always for a little bit more from the technical part, like like checking out the hack projects, working on the hack table. And then even though we did the conference last year at lightning conference, so kind of from that kind of sphere like the project RaspiBlitz project developed.

Stephan Livera:

Awesome. And let’s say from you Openoms.

Openoms:

Yeah. So it’s just joined the RaspiBlitz project I contributed to in, in the beginning of 2018, I have unrelated kind of science background and, you know, being always a tinkerer in, during the 2017 kind of GPU mining enthusiasm has started to build some machines and obviously very quickly, you know got into, got into Bitcoin, got interested in all this. And in 2018 started to build my own nodes, starting with the RaspiBolt project. And then, you know, I got to know the did RaspiBlitz, which as, you know, absolutely been blown away and then you know, started to want to have my own machines, which I had owned already. So that was different from the Raspberry Pi. And then also, you know, put some services which I wanted use, so

Openoms:

Basically started to contribute. And, you know, from that it’s a way of learning for me. It’s a huge journey of, you know, getting experience with this and the related services.

Stephan Livera:

Yep. And can you tell us a little bit about how RaspiBlitz got started? Why was it started?

Rootzoll:

So it started with the lightning hack days we were doing, because it was like, initially it was, let’s get the people together that we know from the Bitcoin crowd. And let’s try this lightning thing out and it’s always the best experience to try something out, to get your hands on. So not just talking concepts. That’s great, but also like, okay, we really want to learn how to run a node, how to be part of this infrastructure. How can we build this infrastructure? What learnings do we do need there? And then we started on the first act that we started with the it was a tutorial from Stadicus for the RaspiBolt. That was kind of a tutorial where you go through line by line Linux code and you set up your lightning node on a Raspberry Pi.

Rootzoll:

And this was a great start, but we quickly learned that this takes a little bit long time to really do this. Its great if you really want to know the details, but we need to get your node ready. We wanted to speed up things. So we started to put it into shell scripts and trying to ease a little bit the pain points for people or doing development, so that they can be a little bit quicker, get to the point, after node running, and then can more experience what it means to run a node and manage a node. And this was a little bit where we like I think on the second hack day or something, we had the kind of first shell script set up there, and this was the beginning of the RaspiBlitz project and I have always have to say like, thanks for Fulmo.

Rootzoll:

Always giving me the time to concentrate also and, and keep on experimenting and making it better. So it grew over time and people started to contribute also. So a lot of ideas came, so we were seeing like, Oh, we need to fix this, or we need to make this better. Or can you make we, can you add this code maybe to the code base? So it started from the beginning like a community project that we try to kept together. So we have other people contributing to the project. It’s not just kind of me or Openoms. There’s also Frankie. There were other people in the past that were on the project. So yeah, it started from this community perspective and grew over time. The code base is now about two years old. So yeah, there’s a lot developed there.

Stephan Livera:

Great. yeah. Look, I think for listeners who maybe you kind of came into Bitcoin and you were only interested in more in the economic aspect of it and you haven’t dived into the technical aspects of it because, you know, running a node can be difficult if you’re not familiar with command line and so on. And I think potentially that’s where something like the RaspiBlitz, because it’s all sort of nicely scripted out for you. It’s a little bit easier in terms of how to set it up, but let’s talk a little bit about the features as well, because it’s not just right. So I guess if you’re just a listener and you’re not so familiar with how to run Bitcoin, you might just think, Oh, just, just download and double click Bitcoin core and that’s it. Right? But there’s actually more to it than that. If you want to use it with say your hardware wallet or if you want to use lightning. So can you just outline a little bit for us? What are some of the features that the RaspiBlitz has and what you can do with it? So maybe Openoms. Do you want to take this one?

Openoms:

Right, let’s say it would be a long list, right. But first of all, RaspiBlitz is, is a full Bitcoin and lightning node. So that’s what it is. Everything is built around and we mostly focused on lightning parts. So first we basically had the RTL that’s the ride the lightning interface, kind of to give it a graphical interface, instead of interact with the LND command line. And then there have been, you know, a lot of other things added and also the scripts are really important, which do help you to set up the node. So there is a streamlined process of generate a wallet, backup your seed, and then sync the lightning wallet to the blockchain. And then it gives you some secretary features of automatically backing up your static channel backups, for example, and also gives you options, to backup update, and also to migrate all those to another node, for example.

Openoms:

So these are the things which should be added. And then, you know, a lot of other projects, which we started to kind of merge in starting from, for example, the lightning loop service or now we have other interfaces, like the thunderhub project, which is another very cool graphical interface for LND. And I, there’s a long list. I don’t even think I can do justice. Yes, it’s, you can see basically everything in the menu. And then there are things which are connected both to bitcoin and lightning, for example, like BTCPay Server which is, you know, based on inaudible and yeah, recently we’ve added JoinMarket as well, which is more like you know, the on chain part. But there are a lot of, you know, bits and bobs in there.

Rootzoll:

Maybe we’ll start a little bit from, because there are a lot of names of projects. So it’s a little bit hard to maybe sort them out, maybe start from what you can see first. So it’s based on a Raspberry Pi, right? So

Rootzoll:

You already said you can run a full node on your laptop, but the idea is really having an always on device, because with lightning, especially with lightning. If you want to be a routing node, you need to be a constant part of the infrastructure. So you have to have your node kind of running all the time. It could be it’s okay, if it’s off or some time, maybe, but the longer it’s on that better. So you need a dedicated device. This is why we’re building, on a such a computer, like the Raspberry pi, because it’s quite cheap, but gives you enough power for it.That’s a lot of node projects to that now, nowadays what you maybe see compared to other node project is that the RaspiBlitz has a little screen on top.

Rootzoll:

So it’s something you stick on top of the, of the raspberry pi and it gives you like a nice optic. So, it it helps you doing set up like a simple things. Like what is my IP on my local network, so I can easily lock into the device. And then from there it takes you into all the software part, like setting it up, setting it up. So at the moment the Rasperry Pi uses SSH to, for the setup and interactive process. So you have, it’s a little bit, you have to open a command line interface, like a terminal, and then you just type the little command in there that is on the LCD display. And from there, it kind of tries to picks you up, even if it’s all ASCII.

Rootzoll:

And it looks a little bit maybe like your interface in the nineties. But it’s, really takes you from there. And then you make your basic setup and then you have all the other apps you can, put on top of it. And there are then even Web UIs like RTL and Thunder Hop, like openoms mentioned, then will give you a little bit more like, and more easier. Like an easier a screen, like, you know, from the browser, how you can manage your node and yeah. From the feature set, there’s just so much it’s really hard, to put it together, but let me go through the list real quick. You have those like say RTL and Thunder Hop. You have a block Explorer that you can run, so you can run your own block Explorer of your, on your RaspiBlitz, and you have a Electrum server there.

Rootzoll:

So that way you can then that’s then for your use so that it can good connection with your hardware wallets. So you don’t have to go to some Electrum server out there. You have your own Electrum server running that preserves, maybe some privacy for you. Then you have a BTCPay server you can experiment with you have that is maybe you can use for running an online shop integrating in your, into your online shop. So you have if you’re maybe online shop online, but you keep the, you let it talk with your, with your RaspiBlitz that sits at your home. And then you have something like Specter where you can experiment was multisignature setup. So we maybe have a Coldcard and a Trezor and then a Specter DIY wallet and you want to experiment with multi signature or setups just helps you in that direction.

Rootzoll:

Then we have a lot of stuff that tries to help’s you manage your node. There’s something like Faraday, like balance of Satoshi, like LND manage. Those are kind of command line tools, that helps you a little bit tries to trying to give you hints, maybe what is a good channel to open or to what channels should I close at something like that. So that different software that tries to get you a little better overview over the network and tries to assist you in your node management, if you want to run your node, a routing node to become a good routing node in the network then you have something like LNBits. That’s the tries to put, you have just one lightning there but it tries to put it into little pieces. So you can, for example, run sub accounts on this, for different purposes.

Rootzoll:

They have a plugin system where you can make it a little POS like point of sale QR codes, or you can give out vouchers to people or LNURL codes or faucets. So there’s a lot of little nice stuff that you can try, to experiment in that direction. When you have mobile wallets, you can connect like Zap or Zeus or the fully noded that tries to manage a little bit more your Bitcoin wallet. So, this is from the mobile wallet. So you can connect your smartphone to your RaspiBlitz to have it a little bit more on the go. And then there is all this exciting stuff we see now happening, with the JoinMarket integration open arms can maybe go into detail that a little bit later on. But also a lot of little features that try to help you on the backup side so you can connected to your Dropbox account.

Rootzoll:

So that automatically encrypted backup is stored somewhere else outside of your home. So even if your home burns down, you have somewhere to go, to find your static channel backup, to kind of regain control again over your funds. You can also have to send it with connect a little USB stick now to make those backups things. So there’s a, lot of little features also in there. That’s really hard all to put together, in a list. So but we try. So when we try to give you a documentation on that and try to give you a little, we try to put you through the journey, like you start with set up and then step by step, you can explore. And maybe this is also why I’m talking to community project and why, came from the hack days, because we try to put a lot of stuff that is developing very freshly. Most of the software is, very experimental still. But it’s in there. So we want to give it, give people that are interested a little bit more into the experimenting side of lightning that they have those tools available, that they can experiment with them and can give feedback to the projects and let them

Rootzoll:

Know what they still missing. And so the projects can improve not every feature there is already like production ready, for your big set up. It’s really, we try to give you a box that you can, very good experiments with the features that projects that are already out there, and you can do your own projects and hack projects yourself and have a good box to work on that.

Stephan Livera:

Yeah, that’s a great explanation. I think for listeners, it might be a little bit sort of confusing and if they wanted to try to run these projects on their own, and if they’re not already quite tech savvy, this is one way you can quickly and easily run a bunch of these different projects, all in one sort of scripted together, experience. Openoms did you have anything you wanted to add there?

Openoms:

Yes,I just wanted to go back a little to emphasize that’s how the way we connect through SSH. So this is like a shell tunnel, which is opening from a terminal. Where do you get actually have a graphical interface, a GUI or appearing? And it has a great advantage over having like a clearnet you know, web interface because it is an encrypted connection and there is no problem of communicating like, a seed or, you know, any kind of secret through this. So it sounds a bit, you know, this is like the first thing the user needs to kind of get through, to be able, especially on windows. I mean, it’s a very native on Linux and Mac, but on windows, you need to usually use an extra application or set up openSSH from the Windows app store to be able to connect. But once this is in you’ve got a very stable, very secure connection. And also another thing about the screen, which is, I mean, it’s certainly nice and, you know, has a very nice feedback continuously so you know it’s up and running, but also it gives you clues during the setup that what to do and what is the next step and also what to type into terminal when you get there. So yeah, I just want to add those as unique features of the restaurants,

Stephan Livera:

Right? Yeah. And so let’s talk a little bit about target user. So, I mean, there are different well-known node projects, right? So for example, the Ronin Dojo is for somebody who is maybe they don’t care about lightning, they just want maximally Samourai Wallet and like Coinjoin and privacy and those aspects of it. And then you’ve got, say the, myNode or the Nodl. myNode it might be seen like more, okay. It’s kind of like the web interface as you were mentioning. And maybe the RaspiBlitz is a little bit more of a community focus, maybe a little bit more of like a merchant use case. Can you tell us a little bit about how you’re thinking about RaspiBlitz as compared to some of the other well known node projects?

Rootzoll:

Sure. I hope I don’t mischaracterize another node project so but as far as I can see, for example,

Rootzoll:

The like you have with the Nodl, I think it’s a very solid box. It doesn’t try to do all the things, but it tries to do some things really good and think , it’s a good thing to go. If you’re more like a merchant and you want to be self sovereign there on that side and have a good physical security and all those little details, thing there is a good direction to go with the nodl. The myNode it’s a little bit more like, I think this is people for the people that mostly expect having a product a little bit more like something, that works a little bit more out of the box thing that you can have to split the other of course with RaspiBlitz too. But the myNode comes a little bit more from that perspective, tries to picks you up with a web browser from the beginning and has like a feature set that where is well packaged.

Rootzoll:

And so you can also try a lot of stuff out, but it’s, but it comes a little bit more with the, with this kind of product, feeling like, so if you really think you’re search for, you’re really not a technical user you don’t think of, so as a techie user, but you want to have lightning then I think the myNode is something that’s interesting for you, the then when we see the RaspiBlitz, I really think it is for you. If you will have a little bit like a technical interest there, I think you need to be a little bit of a tinker, maybe not. We need to our hardware team crash course kind of style, but you least interested a little bit geeky. So, and you’re interested in a little more in the education have a deeper insight maybe, or learn a deeper insight during this journey.

Rootzoll:

How, everything works a little bit like because it gives you this, you can very easily and quickly jump into the, details with the rest of your RaspiBlitz. But so it’s a little bit more for people that want to be educated on running a node that want to tinker with it. And they want to maybe have a little hack on it, develop a little bit on it, have an own project they want to integrate, then the RaspiBlitz is definitely for you. And it’s also for people that like to try stuff out. So if you really think you’re one of those early majority people that really like to try out really this early stuff, and then says, then definitely you think that the RaspiBlitz is something for you to jump in first.

Rootzoll:

So and it definitely maybe to also to add it definitely comes, I think, from the other, compared to the other ones from the DIY perspective. So, because, we offer just maybe to make this clear, I think also the other node projects, if you can build yourself. So they are all open source, but the RaspiBlitz has I think the most direct approach to get, you can get all the single parts and then just put them together. Like it’s all documented on the RaspiBlitz project and we have a shopping list there that you can get all the single parts and then you put them together and we try to help you step by step to get it running yourself. So think from the, do it yourself, perspective.

Rootzoll:

RaspiBlitz most kind of prominent, even if, even if there’s possibilities to buy it kind of already assembled and a little bit more ready to go. If, you know, if you just interested in getting the software running and trying your software out.

Stephan Livera:

Great. So perhaps we can just summarize that as saying, this is very, there’s a DIY feel around RaspiBlitz. And it’s very much around taking part in the different projects that the community, the quote unquote Bitcoin community has. It, there’s a lot of different projects that you can try those as inside your RaspiBlitz, and you can either build it yourself, or you can buy a pre madeRaspiBlitz.. And so let’s talk a little bit around keeping, you know, security of the node. And I think openoms, you’re touching on some of this as well, where at the, from the very start you have to SSH into the box and it’s not available over just kind of the home wifi, if you will. So can you tell us a little bit about that and what are some of the things that we should be thinking of when we’re trying to secure our Bitcoin node?

Openoms:

So this is a very iterative process. The you know, security, and maybe have a good base. And then every time someone would point something out, I mean, it’s happened more, I think an early beginning of the project then, for example, there’s been efforts made that there is this little screen, on the node for example, but, it’s locked down in a sense that you cannot login to users through it. So you cannot use it like a monitor. Even if you attach back a keyboard and mouse, you cannot use it like a little competition and just, go on to your friend’s node and, go and hack around it. But it’s starts from certain compressors, for example. So you see flesh the SD card image, which is provided and PGP signed by rootzoll.

Openoms:

So or, you know, if anyone else would give out an SD card image, there would be an expectation to do so you could verify that, or you could even just build the SD card and the scripts from source. So you can just, if there is a script which you can run, which is that when we are building inaudible image, you can do it for yourself. So you absolutely don’t need to rely on that either. And when you first login, so the screen will show you the IP address, where to where to initiate this SSH connection. And then there is a default password, which you need to change and to first login, so cannot, you cannot do anything else. You are locked in and the screen until you give your own password, which will change the passwords for all the Linux users on the, on your node.

Openoms:

And from then you can to set up and only then you will be coming to the steps where you set up your lightning. Then you will be giving a seed. You will be getting given a seed and et cetera. Also, you have, more, you will have more passwords to note. So there is, sort of call it like a password A is for it’s like domestic password, which is, which is accessing your SSH. So it gives you sudo access, super user access. And also so with that that you can modify anything, but then there’s the password B which is the same as the RPC password. The Bitcoin RPC password. And we use that from the Bitcoin conf we use that to control other services. So for example, you can log in with that password, to the RTL interface, to thunderhub it can be possible for Mac users, et cetera.

Openoms:

So we encourage you to use a good password for that. And also it is like enforced, you need at least eight characters of a password. So you cannot just use something that is very easy. And then there’s password C which is unlocking your, lightning wallet and all of these for that. So, I mean, we have mainly two hot wallets here. The LND wallet, first of all, which is encrypted, not only, is a seed uses a 24 word seed, that is like an passphrase, which we did not really carry on using because that gives some added complexity, which is then might make it difficult to restore. But then there is the encryption password which is which we call Password C and that is needed every time.

Openoms:

You restart your node, you would need to type it in, unless you’re ignoring the warnings. You want to activate the auto unlock feature where it would be obviously need to be stored on the node. And then it would be automatically unlocked. So I mean, we don’t keep so there are nodes, I mean, more specifically, the nodl, or more specifically the samourai version, which does encrypt the discs, I mean, we did look into this and there is like, you know, this is something which would be a very nice feature, but also we need to think of what tradeoffs are there, does it come to? And how would that limit us to be able to restore in a kind of failure, especially if we have, you know, we have no control over what kind of hardware they use. So not everything is encrypted, but the wallets are, and also all the interfaces are kind of guarded by a password.

Stephan Livera:

Yup. I guess, just to summarize for listeners, just to make sure that people can follow along, basically what you were mentioning, there is some of the passwords around access to your Bitcoin node. And so typically you would set these in your Bitcoin.Conf file. And that includes the RPC and RPC means remote procedure call. And the idea is internally inside the system, there’s kind of different authentications now for listeners.If you’re not technical, don’t worry, like the wizard walks you through this. Right. But we’re just trying to talk you through, so you understand what’s going on in the background there. And also what about just, I guess, on the local network I presume you’ve got cause I think even Zelko was borrowing some tips from you openom on UFW wasn’t it the I forgot the exact, what it stands for something firewall, uncomplicated firewall.

Openoms:

Yeah uncomplicated firewall. So, I mean, we do use the, like the basic hardening measures, which can be done, on a Linux computer, which is, you know, by, I mean, by nature is much more securce, than any of the windows computers at hand. Right. And, and also we do, so when just setting up the node and then we are running this builds with script, we are removing a lot of unnecessary packages, which are sitting on there being in the raspbian these through, but not needed for our use case. So yes, there are two things mainly, which is the fail2ban application, which is called like fail2ban which stops an attacker being able to brute force the password or the SSH password in this case.

Openoms:

So it was after three tries, it would ban for like 10 minutes. So, you know, people sometimes come to us saying, Oh, I cannot log into to my node. Although I’m not sure about the password. Well, then, you know, you have a need to need to wait another 10 minutes and maybe another one afterwards. And the UFW the uncomplicated firewall does just makes sure that only the ports which are used are open. So in the install scripts and the uninstall scripts, we opened the ports, which are needed, for example, 3000 for RTL. And if user would uninstall the application that that’s would be closed again. So this is again, just a kind of a measure on the network to see, because we cannot really, I mean, it would presume that someone’s home network is safe ish, but that

Rootzoll:

Is no, there is no guarantee today that then, you know, there’ll be all kind of internet of things. And these things are listening and snooping and trying to collect data on it. So yeah, just need to do the basics.

Stephan Livera:

Right. And so we can understand that as we’re trying to where possible minimize the possible attack, ways that somebody can get into the machine and try to take the secret or monitor it or things like that. Also I think it’d be great to talk a little bit about if you want to operate your node remotely. So let’s say, you know, I buy the RaspiBlitz. I have it sitting at home and I want to use lightning while I’m out. You know, how would I do that?

Rootzoll:

Yeah. I think just, this is the place where you normally connect a mobile wallet to too. It’s also, you have your smartphone and you want to connect to it. To your node. There are like Zap Wallet it’s available for iOS and Android. There’s Zeus wallet. That’s also available for Android and iOS and sendmany app, it’s a smaller one, but it’s also available. So those, and those are the wallets we support. So what you do is once you set up your RaspiBlitz, that’s you just go to the mobile and say, I want to connect my smartphone. And then it gives you a pairing code, like a new scan pairing code, then with the specific smartphone. And then the smartphone can securely connect to your RaspiBlitz. That’s how it should work. But now it comes the complicated part that you behind your internet router.

Rootzoll:

And normally we weren’t, this was not built like that. You can, the idea was that we are consumers now right. So, we the idea was not that we could we should provide services to the outside. The internet was built for that, but the internet providers have different ideas. So it’s a little bit that comes some technical problems. So of course you can connect it for your local network, like with the pairing code, and then you’re on your same wifi, no problem. But then a mobile wallet makes no sense, right? You want to go outside and have it from, the outside. And there’s a lot of a long journey. We, try to build solutions out. So first of all, when people can configure the router, of course, there are some, there’s a possibility to forward ports, so that something from the outside can go to directly to where this wallet needs to talk to, but then you need to control over your router.

Rootzoll:

You have to need to be able to configure this. Some people can, but not everybody can. So if you, use the wifi from your neighbor’s house, for example, you will not be able, to open a port to you. And a lot of internet providers also don’t allow your or completely shield you from the outside. And doesn’t even give you those, this possibility. So this been our work for everybody. So then there was the idea like why not use Tor? So, you can, it’s the idea that you can run a complete RaspiBlitz behind Tor. And then also this does wallet gets a hidden service address, like a port address, like, you know, from various Tor websites you can call. And the good thing is those addresses are then reachable day. They kind of tunnel through your router, like Tor has, this can do this.

Rootzoll:

So, but then you go, mobile wallet can just talk to this Tor address. Some mobile wallets try to integrate Tor now. So Zap wallet tries to do this other wallet you can use with a proxy program that you can have on your smartphone. It’s a little bit hard to set up, even on my smartphone. Sometimes it’s a little bit of pain to get this working. So this also is a step better, but still it’s not the easiest out of the box solution for everybody still. So, where we were going now, a little bit more is into this developed a service called IP2TOR. So this started on, one of our hack prints on our online events of the hack days the idea came up and also like Stadicus that built the RaspiBolt tutorial in the beginning, and was building, on the shift.

Rootzoll:

Crypto BitBoxBase had also this idea, how can we make it easy? Maybe we can use Tor to get out, to get easy outside of the router, and use the anonymity that Tor gives you. But then to the outside world, we can do as a service somewhere that then gives you a public IP, like rents you out, kind of an IP and the port address. And once you have that, you can very easily, like when you activate that you can very easily like just the QR code, scan it. And then wherever you go, your phone will be able to connect to your RaspiBlitz. So this is a way not just from the mobile wallets, but this is one of the first applications where you can see the benefits that this kind of service now integrated can help you out a bit, on to make it more easy.

Rootzoll:

And so that you don’t need to do all this configuration part on your infrastructure. And even if you’re not possible to do this, that you have a way out and an easy way to do this. But we have to warn, it’s a subscription service. So this is something then you pay for. But, it’s not something that the RaspiBlitz project is it’s running just for themselves. It’s an open source project. So anybody can set up such a shop out there. The RaspiBlitz, the next version would come out with shop from Fulmo that is kind of paired default in there, but you see, but you can exchange it with every other shop address that could be out there in the future. And then you just choose a bridge there. It’s still a little bit technical, but at least we’re trying out the technical concept now, and then you can really just pay this, for a day.

Rootzoll:

Like you paid 40 satoshis for this. Right. The good thing is we have a lightning node here, right? So you can pay services around that. That gives you additional infrastructure. You can make, may make payments there very easily to rent such services. And we can make very small transactions now, like 40 Satoshis for, using it for a day and then it can, then it will automatically make the recurring payments if you really liked it, if it’s working for you. So try it out for one day. If it’s not working, you cancel it. But if it’s working for you, can keep it running. And we’ll kind of make little small micropayments and a subscription base to use this infrastructure. So you have not a lot of upfront risk you also have. And the good thing is about the service. We like a lot is you’re using Tor right.

Rootzoll:

To connect to it. So you are an on anon site there. So nobody, we don’t know who you are. We just see a Tor address we should forward traffic toward, we running the shop at the moment. So, and then you pay with lightning and we also don’t know who pays us. We just see we got paid and now for service to try to forward those traffic, to RaspiBlitz, to just one Tor address. And so, this is a very nice set up where all the benefits, we hope that from lightning come together and give it it an anonymous use case. And we have this micropayments for small infrastructure. You just pay for the infrastructureyYou need a little bit, and this also, IP2TOR can then enable other web services.

Rootzoll:

You can also run on your, on your RaspiBlitz and want to have it easily accessible from the outside. So, this is a little bit the journey like where, but it’s not that easy because again, the internet that we use was not built so that we run the service at our home, but in the end we can do. The bandwidth is there, the technology is cheap enough. We have now projects also in other kinds of projects, you can see more and more, this idea comes. I don’t want to have everything in a cloud. I want to have stuff at my home. And so step-by-step, we kind of gaining this territory again.

Stephan Livera:

Yeah. That’s really interesting. And very clever approach of trying to, in some ways, get the best of both worlds. And so if you are a user who wants to run a BTC Pay shop at home this is another example. So I guess there’s probably the two main examples that I’m thinking of. Say, one is you’re user who wants to connect back to your lightning node at home using Zeus, for example, on my Android phone, this is something that can help you with that to make it a bit easier. And then the other one is, if you want to run, if you’re a merchant and you want to make it so that the outside world, somebody just types in like a normal website address, but really in the background, it’s actually going to your RaspiBlitz. And that’s where you’re doing the actual sale of material, right. Or whatever you’re selling.

Rootzoll:

Yeah. Well, but we had to solve one, one last bit there, because this was exactly the point for the, for the mobile wallets it’s not a problem. They, use their own certificate to secure the communication. But when you were talking about services like BTC Pay, for example, which is a website, you kind of serve we also needed to take care of this does this end to end encryption encrypted, right? So because there would be, if you don’t would not use this HTTPs, there would be parts that are going over the internet, people read. And we don’t, nobody wants that today. This is,10 years ago. So, but it comes to the last part, so that a normal web browser should work in a normal web browser. And so that those that you get this little HTTP secure sign there, you need to use a SSL service that is accepted by browsers.

Rootzoll:

Normally you can make a self certificate so you can create, just create it yourself, but then every browser will just want you “This is an unsecure service, don’t use this”. And then a lot of people would be scared off, and then this would not work. And a lot of features, you cannot then use in the browser, like using the camera and all this stuff that might be interested in for some services. So what we had to solve was also that you can use Let’s Encrypt, for example, it’s a free service out there where every web, everybody that runs a website can get a free certificate so that it works in your normal web browser for the people using the website. And now you can use also the on your RaspiBlitz, you can also make a let’s encrypt subscription now, for your, for example, for your IP2TOR address that where you then serve your, BTC Pay server. Then you can go into this merchant direction or what is the other project we now have in 1.6 that will easily integrate with IP2TOR and Let’s Encrypt is the LNBits where we hope to make some little bit more services to your local community possible that that RaspiBlitz can serve. And you can maybe get a little bit more active with your local community and provide Bitcoin and lightning services.

Stephan Livera:

So can you tell us a little bit about what LNBits offers there and how that works?

Rootzoll:

Sure. they’re kind of two concepts there. There’s a lot of other stuff you can do with, with Ellen bits, but there are two concepts kind of, we’re interested in a way we can see it can make sense, to run a RaspiBlitz for you and for your local community. The one is on, do you remember, you remember like paper wallets, right. Which we had in early on and big Bitcoin, and like to pass around to onboard people, to just give them their first satoshis or maybe was not a Bitcoin, but it was at least some amount on there so that as people get interested. So it was a nice way to do this, because lightning, this got complicated again a bit because yes, you can normally you have to install a wallet there, and then I will maybe send something from my mobile wallet to your mobile wallet, but we don’t have this.

Rootzoll:

I can get, can give you kind of a voucher gift card there that’s and with LNBits for example, by using LNURL, we can create vouchers again. So little QR codes that are just static, that you can print out and give somebody. And if this person scans this QR code, this person can get the satoshis on there. And LNURL, some mobile wallets support LNURL, and then they can directly, so you scan it just with your mobile wallet and it directly gets, you get the satoshis from my RaspiBlitz, right? So, I give you kind of vouchers. Satoshis, I give you allowances little allowances over Satoshis out as paper that you can then use. But the LNBits puts it a one step further because not everybody has a mobile wallet installed already, right?

Rootzoll:

So people just see a QR code there. And what LN URL allows, this gives you give, put a fallback URL in there. So if you just scan it with your normal phone and most camera apps, now, do this, as you point at the QR code, and it says, Oh, there’s a web address in there. Do you want to open this? Say, okay, I open this and then it opened up the mobile wallet that is served from Ellen bits, from your RaspiBlitz from your home. And it’s like a temporary wallet that you get like a web wallet that is instantly there for you like that you can then use, and you can even spend it from there. So it can then can make use of the camera of the smartphone. And you can directly go somewhere, for example, buy something with that.

Rootzoll:

So, and it’s an easy, it’s a very easy way to onboard people to let them without explaining them. You have to install a wallet first or whatever. You just give them the paper. You can put it into postboxes for example, just go around your neighborhood, putting put, make a nice flyer, put a QR code on there. So this single QR code for everybody, but you just print them out on stickers and you put them, put it on flyer, you put it into postboxes and let people know this is your first Satoshis here. Take care about them and transfer them somewhere safe where you can use them. But, it’s a gift to, onboard people. This is the one side, for example, that you can do, like educating people, like owning their first kind of Satoshis and you do this with your, really, with your own RaspiBlitz at home.

Rootzoll:

So you don’t rely on a central service for that or something. Everybody can start in a very decentralized way with that. The second part that we’re little bit aiming for is the we call it cash in the bag. It’s maybe not the best name right now, but the thing is, it gives you a little bit the idea it’s it’s about merchant onboarding. It’s the idea like you have little stores in your neighborhood. Normally you have some social trust to them. It works. You need some social trust there because what you do is you can take a little bag, you put fiat cash in there, some just dollars or whatever, like euros, and then you give it to them to themerchant. And what you also do, you put into this little bag from the LNBits, there’s a plugin called TPoS also a little QR code, but this QR code now is it’s like a URL, a web address.

Rootzoll:

And when the merchant just scans this at, the store, it opens a point of sale UI in the web browser, just, as a website. So no app needs to be installed. So if somebody comes to the store and wants to pay now with Bitcoin, the merchant remembers, Oh yeah, I got this bag here from this friendly guy I like. And so, yeah, you want to pay with Bitcoin? I take the back, I take out this QR code, scan it, and now I have to point of sale in my store, I present a type in what the customer has to pay. I present it to the customer, the customer then scans that paste, that invoice was created. But this Bitcoin is not going, to the merchant. This bitcoin or Satoshis are going to your RaspiBlitz.

Rootzoll:

But the merchant now can just say, okay, there was five us dollars, for example, that you just paid, I see that it got paid. And now I’m allowed to open this bag and take the fiat out like the five US dollars and put it into my normal register. So, nice thing here for the merchant, nothing changes. The register stays the same, the whole process the whole bookkeeping stays the same, but, because you’re taking like care a little bit of this first complex steps, like running a node, giving us having account running here. So, you buy in the end, the Bitcoin from the merchant, like if somebody pays with Bitcoin, you buy this Bitcoin from this merchant and directly give them the cash upfronted the cash it’s already there. And just this makes it very easy thing for people to get started.

Rootzoll:

It’s not a solution to onboard merchants with large volumes, but it’s something where you can get started. So from a merchant can, can try it out without risk because you’re upfronting the money. Right? So it’s, I think it’s, I cannot think of an easier way to, get people into the talk of, Oh, why not accept Bitcoin at my store? And so these are two things you can do for your local community then with the RaspiBlitz using the Allen bits, and you can run it securely behind Tor and, but have it available to the outside with the let’s encrypt certificate through. So through something like this IP2TOR service. So they, the little pieces come together where we can see a good journey where RaspiBlitz can also go and deliver additional services, for you. And maybe why you are running a node, not just to be routing node also to deliver, some services to your local community.

Stephan Livera:

That’s very clever. I like the idea. And so basically you are setting up some of these merchants with a small petty cash amount. Like it might be a hundred dollars or $200 where something small and you know them. So it’s kind of, there’s some level of trust there. And then they can start at a very low investment level in terms of work required to accept Bitcoin. And so that’s potentially something that you can try and as like a little way to kind of build your local community, I just wanted to confirm then, so would that be lightning only? Or could they also just do, could the customer in-person at that point, do an on chain payment there?

Rootzoll:

Technically that could also be on chain payments, but we don’t have this feature in there. So at the moment it’s con it’s concentrating on lightning, especially with we talk small amounts. If you can start with something like putting 20 US dollars in that bag. So I think Bitcoin transactions make sense now in store a little bit, like feeling like from 10 US dollars, we below that we want to try out lightning and meet maybe even, I think it’s a good starting point, technically it’s possible. And if somebody is very interested in said, I love this idea, and I want on chain Bitcoin in there. Let’s talk because that’s exactly why, this is an open source project, but we just have a limited amount of time. And I think the lighting part was the most reasonable to start.

Stephan Livera:

Yeah. And you know what I think that might also make sense for when people are doing those little farmer’s markets or just kind of little markets where you’ve just got a stall and you’re just temporarily setting up for a day and you might want to be able to take lightning. And you’re selling small little things that cost, you know, $2 or $5, something like that. That’s probably a good example there where if you had, if that merchant has say an iPad or a tablet, and then they just use that for the web site, and then the customer is just scanning and paying with whatever lightning wallet they’ve got. That might be another way where you can quickly set up a lot of these merchants and all they need is their own phone or tablet to take the payment with, and you give them the bag and off you go, right. And then you’re kind of, you’re starting,

Rootzoll:

So, you have no hardware costs, right? We normally we talk about a point of sale or something, and then you have to put hardware out or everybody has to install an app first and then another app to install. So this is really just a QR code you, give out to them, and then you can have small instructions on this card, like, Oh, somebody wants to pay with Bitcoin, go there, scan this. Punch in the amount I think, that’s, it’s very easily easy steps to follow,

Stephan Livera:

Right? Yeah. Yeah. And just around hardware more broadly are there any, I guess, what are some of the considerations for a user out there when they’re building a RaspiBlitz? I guess the one key consideration might be the choice between using say a hard drive versus an SSD solid state drive. Right. Because there’s a cost consideration, but then also one’s more reliable and more performant, more efficient than the other. Do you have any thoughts around that that you can offer for listeners?

Rootzoll:

Yeah. I think openoms is going to give more details, but I just want to mention one point because we tried to let out a lot of hardware stuff as, but, and I like because it’s a do it yourself project, it comes from a do it yourself, approach. People like to use the hardware they have lying around. But we really want to say, take a look at the shopping list that we have on the RaspiBlitz website, because that’s, this is the hardware we kind of most tested and have the, best kind of feeling, to recommend to you to use because there are some hard drives, have different kind of, power consumption and stuff, but this is exactly something wherever openoms can give you more details.

Openoms:

Yeah. This mainly comes from the community. So, you know, I like to test for myself and, you know, use a couple of things which are either running around or, you know, I get some new new hardware. I mean, I started with a hard disk and then, you know, managed to,

Openoms:

This was before the static channel backups that managed to fail. And then, you know, I lost some satoshis, a typical story. You know, I mean, this has been a donation out to the network, because there’s no way to recover them. I still have the pub key, you know, I can look at it, right. It is what it is. And the big advantage of the SSD or the solid state drive that it doesn’t have a spinning disc in there. And even if it has the hardware, if it has like a power failure or and call it reset, you know, sudden shutdown, when you put, when you just pull the plug it won’t hurt physically. I mean, and even if it does kind of mess up the file system, it’s usually more easily bearable obviously than physical damage. So for that reason to be on the safer side, I would always use an SSD, which is also a good quality one, but you need to be, as rootzoll said.

Openoms:

You need to be aware of the different kind of power consumptions, and also they might need, so some of them still might need an external power source because to be the most compact package, to have the most compact package, we try to power everything from the rest through the raspberry PI. So we put just one power plug in there and then through the USB, the SSD would be powered, which is, you know, it’s not the way they are designed, but a lot of them can take this and working reliably for years, also in regards of the size, we recommend a thousand. One terabytes, right? Because to fit everything in there because I mean, all of us started with 500 gigabytes drives and then with the Raspberry Pi 4 it’s it’s particularly in the sense that you need to be very careful about which kind of connector to use between the USB port and the, and the disc, because most of them, especially old ones already fortunate that the cheap ones don’t do it because they’re not compatible with the standard.

Openoms:

The Raspberry Pi itself is using. But if you’re getting it right, you know, you can download the blockchain in like two to three days. So it is a huge difference. Whereas with the using hard disk, it would be at least a week. So that is a big advantage in there, so that it maybe costs now maybe one and a half to maximum of two times, of a hard disk. But you got better reliability and speed.

Stephan Livera:

Yeah. I guess for me, when I’m speaking to a newcoiner or I’m trying to teach someone how to get, do, get into Bitcoin, I sometimes face that because you’re trying to think of something that you don’t want to push too high a cost on to them and say, Oh, you need to go and get the best hardware. So, part of me, you know, part of it, and we probably want to try and tell them, Hey, you can just start out with something cheap. And then if you’d like that, then kind of move further up. And then you might have some other friends who are kind of, they’ve already got lots of money and it’s not a big deal for them to go buy an SSD and the more fancy hardware. Right. So yeah. One other, one other point I thought would be interesting to discuss is just around a future hardware trends, right?

Stephan Livera:

So I think right now most people are, they’re comfortable with using Raspberry PI’s even though technically it’s not, fully open source. And so there are some in the kind of Bitcoin world who are more hardware and security focused, and they’re talking about say, Oh, we need to move towards hardware that’s not potentially backdoored and things like, you know, Raptor open source hardware and things like that. But the, obviously the trade off is that stuff costs a lot more. It’s not, as, you know, it’s larger, it’s not as you know, easy. Whereas right now the easy kind of node solutions are using things like Raspberry Pi or the rock 64 and things like that. So just curious on your views, do you see it, like for a couple more years, people are just going to be using raspberry pis because that’s what’s cost effective and then potentially in the future, people will be moving towards more of those open, like the open hardware?

Openoms:

Yeah. I mean, this is a huge topic. You know, there’s no such thing for us, unfortunately at the moment, which is fully open source hardware. So that is a scale, right? So, in there are more open source single board computers like the one from Pine 64 or from hard kernel, which are called Odroids. You know, I like those very much, but you know, the compatibility and the support is not really comparable to what the Raspberry Pi has. And also all the software stack we are running on top is fully open source. And we, you know, try to verify, I mean, we verify as much as possible or building from source or, PGP or through the, Linux repositories. So, you know, there is some control we can give, even if there is some partially closed source firmware running on the chips, for example, on the GPU of the Raspberry Pi, you know, that cannot really do much. And I mean, if you would think of risking, I mean, now we are capable of running like a routing node, and you’re going to do coinjoin and things like that. But if you’re thinking of putting back partly thousands of dollars worth of money that will be going there, that it might be.

Openoms:

You know, Raspberry Pi might not be your thing. This is, yeah, this is not for the life savings, but I mean, the capabilities is almost there. So, you know, I mean, everyone needs to kind of that’s when you throw it too, when you think of like a, keeping the money in a paranoid, cold storage set up, right. Rather than, in a hot wallet in a, in a little, you know, a hundred dollars computer setup or like $200 altogether. So the trends I’m very hopeful to see some things actually like RISC-V and begins small microcontrollers already appearing, which can be fully open source. But I think for now, as it looks at our supplies, a very good base to build on or the, you know, I’m experimenting with other stuff. And I like to share this with anyone you know, the interest is not there that much.

Stephan Livera:

Yup. Yeah. And I think it’s a totally fair point because we have to be pragmatic as well as that. We can’t just go out to saying, Oh yeah, everyone needs to like go for the maximum possible. I think it’s also going to be about, what’s compatibility and figuring out when you’re helping somebody what sort of pieces of hardware are well supported. And that there’s a lot of, there’s a big community around that. So it’s easier to find, ask questions and Google things and ask things where yeah. But I think potentially that is something that maybe all the Bitcoin people will be moving towards in future years. Once it, becomes a little bit more feasible, I would say what would, what do you guys think?

Rootzoll:

I personally think that the Raspberry Pi is great because even, if you make this experiment with running a full node and after, I dunno after months of something you see, okay, this has maybe nothing, not nothing for me or something I learned maybe a bit, but okay. That’s okay. I learned my part. Then you can still make use of this Raspberry Pi very easy because there’s so much other projects that are, there’s a whole maker scene, around the Raspberry Pi. You can give it to a friend or you have your viewers and we’ll be happy because he has already three ideas, what he can do with that. So I really think just as the Raspbery Pi as a good starting board, and I think it’s the most reliable, like little small computer also from the price point. it’s very good from the processing power.

Rootzoll:

Now we have a good setup. And I think from the setup we have right now for the rest bullets is something that it’s a good solid base even for the coming years. But, openoms already experimented with other hardware platforms. So once there are some nice open source board that really at least makes it possible to, also see all this stuff fulfilling that we see for the future. And we wish for a future, like open source hardware, then I think just, as something we definitely then build with, try to get into the direction. But I think for now, and also with the limited kind of amount of time you have for testing and all this stuff, I think we have a good, found a good home was the Raspberry Pi.

Stephan Livera:

Yeah, of course. Yeah. I totally think it’s a good option for people to look at. So yeah. Give us the give us the, I guess the pitch, why, if somebody is a listener and they haven’t set up their own Bitcoin node, why should they, try RaspiBlitz?

Rootzoll:

When you haven’t put up your node, I always say like, we know not your keys, not your Bitcoin. Right. So I always like to say, not your node, not your rules. So there are there’s at least having the experience. I think not everybody needs to run a node about, but I think everybody should at least make something. Especially if you’re now in an early Bitcoin scene, you really liked the avant-garde of technology. We all hope that it’ll be more mainstream soon. Then, I think it’s a good education to learn what it means to run a phone. Or even if you just do inaudible on your, laptop, that’s also a good start, but then we leave experimenting with, such a hardware. I think this is definitely something I can recommend because it gives you this feeling of really running your own service and your own server.

Rootzoll:

Like you really, you starting to, really run your own machine there at home. And just, this really gives you a, gives you a good experience and especially the RaspiBlitz. If you’re, if you’re I think a lot of on, when you go to a Bitcoin meetups and you bring a little RaspiBlitz with you, I think it’s always a great topic to get people started because you are, you always, it always brings people together. And this is definitely something we see like on the hack days and all this experience, like this is a project and people like to connect on and exchange ideas on. So, it’s always a great starting topic to also do to for meet ups and to talk to other people in the scene.

Stephan Livera:

Of course, openoms, anything to add?

Openoms:

Well, this is pretty much the approach I came to as well, but I mean, it depends how much you want to and how much you value, you know, a couple of satoshis but you know, it’s a great feeling that you can actually generate some yield on these things. You know, it’s not significant, but you are able to run a routing node and, you know, just a feeling that you’re actually contributing to a decentralized payment network and there are payments going through or through your node, is a huge thing. And, you know, you need to start small to be able to participate big in the future. So I think that this, it makes people very I mean, you know. And then, you know, also is now not only having the lightning but of it, but we have the JoinMarket, which is, you know, as you probably know, or the listeners know that is this maker taker model, that you can offer your coins as a liquidity for CoinJoins as well, that you can generate a little bit of income and also improves your privacy.

Stephan Livera:

Fantastic. So if listeners want to find you online or they want to get a RaspiBlitz, where can they find you guys?

Rootzoll:

I think you can find the project on Github. If you just type in a RaspiBlitz or type in RaspiBlitz into Google, you should find it. There’s a short link like RaspiBlitz.org. So this is a website, at least then you find all the, maybe the most important links. There’s if you want to just pick up a RaspiBlitz like, ready made, then I can recommend to you the Fulmo shop at shop.fulmo.org. And there you have some, you can order, the parts all in one package. But again, the shopping list is also on the project side, if you want to want to buy everything by yourself. I’m Rootzoll on Twitter. So I think there where can I try to keep people updated on the project and Openoms?

Openoms:

Yes. So I have a little shop Bitcoin only running as well.

Openoms:

It is at the domain diynodes.com if you would be interested in not spending fiat, but some bitcoin, you know I do offer the most kind of successful set up of mine there as well. And then, you know, I’m very happy to talk about these things further, you know new projects, and just really anything going on. Most of the kind of popular social media in Bitcoin circles, which is mainly Twitter, Telegram, Mastodon, Keybase, you know, that’s, I’m openoms over there. And github of course.

Stephan Livera:

Excellent. Well, look, I enjoyed chatting with you guys, and I think that it’ll be really great for my listeners to hear a little bit about the RaspiBlitz. So thank you for joining me guys. And listeners, you can find me at stephanlivera.com. That’s it from us. And we’ll see you guys in the citadels.

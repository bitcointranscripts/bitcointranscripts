---
title: Extreme Opsec For The Modern Cypherpunk
transcript_by: Bryan Bishop
tags:
  - privacy-enhancements
speakers:
  - Jameson Lopp
---
Jameson is the infrastructure engineer at Casa. Please welcome Jameson Lopp.

## Introduction

Hi fellow cypherpunks. We're under attack. Corporations and nation states in their quest for omniscience have slowly stripped away our privacy. We are the frog being boiled in the pot called progress. We can't trust that corporations will grant us privacy out of their beneficience. Our failures here are our own. After being swatted a year ago, I set out to restart my life with a new focus on privacy. There are not many resources out there for how to achieve what I want.

It's important to note that the goal of this presentation is not how to disappear, though that is a good book I recommend reading. If I wanted perfect privacy, I would have closed my online accounts and reappeared as a pseudonym and stopped appearing in public. My goal is to achieve the best possible privacy while still maintaining my reputation and be able to participate in this ecosystem as myself.

## Security and privacy

I will not have time to discuss physical aspects of security. Another thing to note that a lot of this advice is specific to jurisdictions. I will reveal that I do live somewhere in the United States of America. In general, when looking at privacy resources, most of them are written for Americans, and this is because more of them are under attack by frivolous lawsuits, jailed for homeland security charges, and surveilled more.

Justine Sacco tweeted out a bad joke on twitter before she went to Africa. She found out she was the #1 twitter topic worldwide after celebrities denounced here. Her employer, a NY internet firm, declared that she lost her job as director of communications. At least one user photographed her at the airport. In the information age, it does not take much to attract the ire of millions of people.

In bitcoin, we have a long history of physical attacks against bitcoiners dating back to the first contributor who worked with Satoshi, Hal Finney, who was harassed for many months and extorted for quite a bit of money, culminating in the swatting which resulted in him having to be outside in the cold winter night while he was dealing with ALS and basically parapalegic or possibly quadrapalegic.

There are quite a few other more recent attacks as the bitcoin price has increased and there has been mainstream adoption. In fact, we can see this has been the results of an open-source repository that I have been running... there seems to be correlation between physical attacks against crypto-owners and the market price spikes and awareness of the industry. It seems commmon sense that as the ecosystem becomes more mainstream, criminals are going ot be aware of this and they will be calculating their risk-reward ratio and they will be attacking people who talk publicly about crypto. This catch-22 is actually a result of the fact that once you get into this space, you're incentivized to want to talk about it to other people, to understand it better, and to build on it. As soon as you talk about it, you become a target. After doing this for a number of years, you have posts from 3, 4, 5 years ago and criminals are doing the mental math about oh this person got in when bitcoin market price was X dollars and now it's worth Y dollars so they might be a juicy target.

## Levels of privacy protection

How much resources is your attacker going to be put into trying to find you? And therefore, how much effort do you want to put into requiring a certain level of resources to be spent? The ultimate one is a nation state attacker. If you're hiding against a nation state attacker, I can't help you. But we can come to an understanding of how to make it reasonably difficult for the average troll on the internet who knows how to get into various leaked databases to make it difficult for you to be found.

Some of the resources I used for this were books like how to disappear and how to be invisible. We give a lot of personal information up. Whenever you interact with a different service provider, you're probably giving name and address. Over your lifetime, you've interacted iwth thousands of databases. Just from the sheer magnitude of different replicas of your information on the internet, some of them are going to get leaked or end up in databases that can be used by dark web searches or investogators sometimes use services for that information.

## Protecting your physical locations

The goal is to prevent any of that data that connects your name and your physical residential address and to keep these things out of databases. The solution is gneerally to use proxies of all kind, including electronic, legal and physical proxies. You need to have the ownership of  your residence in someone else's name, or under an LLC its own legal entity, trusts, some sort of legal entity to shield your name from being listed on various public documents of ownership of these things. You will actually find that... I spoke to a bunch of the European speakers last night; this is highly jurisdiction-specific. You should probably consult with a lawyer about this. Europe does not have good privacy protections with regards to creating legal entities. Even in America, it's not that great. There are only two states for this in the US- Wyoming and Nevada. There's someone who does Wyoming-specific entities, where this lawyer sells privacy as a service, and he uses 3 trusts and an LLC, and makes it hard for people to puncture multiple barriers. I hear Lichentenshein might have some good privacy options in Europe.

Also, you can't backdate any of this. You can't apply this to your current location, which is already burned. Once you have a good setup, you need to not leak other data. If you are livestreaming, you want an audio-proof box that would prevent outside sounds from leaking your location. And on photos you need to look at EXIF data, and you need to strip that out. If you want to get really extreme, then you will have to worry about temporal analysis of things like bitcoin transactions or when you login or tweet or something and how long it takes you to get home. This only matters if you're at a longitude which doesn't have a lot of land mass.

With regard to living in a place that is owned by some other person, this works well for a lot of people who are transient or don't have specific attackers that they think are coming after them, but they are just trying to protect themselves in general. But if you're in my situation where you think someone is causing you harm, then you probably don't want to put your family member in harm's way. You should not receive any deliveries or services in your name at this residence; same for utilities.

You also need to worry about any documents at your house, you don't want to put them in the trash without shredding or burning them. Also, voter registration is not an option. If you want privacy, then you need to give up voting and being in the voting records.

A few years ago, there was a secret art installation with a video feed on it. 4chan was able to track down the location by looking at the planes flying over head and they cross-checked that with public flight information. Next, at night, they looked at the position of the stars and narrowed it down some more. The final bit of info was some random 4channer who was driving in that general area and honking their horns every few minutes until someone found it on the feed and that's how they found the location. Don't underestimate the power of the internet.

## Use mailing address proxies

You never want to associate your real name and your residence. Once the association is made and put into any database, then you should consider that compromised. You might have issues with proving that you have a residence, so you might need a cheap RV lot or something for those purposes. You could talk to an attorney, or look at virtual addresses and remailing services. The downside of the remailing service is that they are in databases themselves; you can't use a commercial remailing service as a proof-of-residence and they get rejected. So you need to use an apartment or RV lot that is not in one of those databases.

## Mitigating realtime location tracking

It's really tricky when going around in the real world; the proliferation of CCTV is pretty terrible. We walk around with phones in our pocket. Disable as much location tracking on your phone as much as possible, which may or may not happen even if you tell it to turn off. Of course, keep GPS turned off. There's a "justice cap" with infrared on it that emits infrared at cameras. The reflectacap reflects infrared at cameras to cause blurring. There's also infrared glasses to screw with facial recognition. The problem with all of these is that they tend to only work in low-light conditions. If you're a nightowl and only going out at night, then this might be fine. For day time stuff, use a cap, sunglasses and a hoodie. You don't want to be walking around with a mask on, because that gets some attention and stare and it's actually illegal in some jurisdictions.

## Protecting real property

You have to have protection for your lambos. Publicly registered property is searchable on websites from local municapalities. You want legal entities to own these different things, and you don't want everything to be owned by the same legal entity. You want one legal entity per piece of property. Say you get into your lambo, they get your license info, and a private investigator does the search to find who owns this car and where is it registered and they might find it's owned by LLC z and then they do another search and try to find everything owned by that LLC and if your house is also owned by that LLC then congratulations they just found where you lived even though you have all these legal entities setup.

Tax records in America are generally not public information, but there's 60,000 IRS employees that have access to that information so I wouldn't call it private. You probably don't want your real residence on your taxes, and as far as I'm aware, that's legal.

Pets are also considered something that have to be licensed and taxed and anothe rsource of legal trails to go and find you. When you have vehicles owned by corporations, then you need to get commercial fleet insurance which is tending to be 2x as expensive.

## Protect your real name

Wherever you live, you're going to have to interact with service providers and repairmen. There's no real reason to give them your real name. You might as well come up with a pseudonym. You want the pseudoynm to be common to the area you're living in, and unmemorable. The best thing you can do is look at census data and find the common names and just pick one and use it with everyone because otherwise you're going to get confused about which pseudonym you gave to which provider. Namey uses the US census data. It's not like these service providers are going to ask you for your government ID: nobody has ever questioned me on the pseudonym, unless you're purchasing an age-restricted item, don't expect to get carded.

## Keep a low profile

Hide in the crowd. Don't stand out. If you have a mohawk or blue hair or a foot-long beard, you should probably think about getting rid of it ((laughter)). Don't wear flashy clothes, don't drive a lambo around, don't do stupid modifications to your cars like stickers or bitcoin hub caps. You want a run of the mill lifestyle that anyone has a second glance about.

## Protecting your privacy online

This is a whole other can of worms that could be its own presentation. Don't just use google or yahoo, use duckduckgo or startpage or several others. Get as many of these privacy protecting browser extensions like privacybadger, https everywhere, ublock origin. Use protonmail instead of gmail. Use VPN like Private Internet Access. I use a VPN to mask my geographic location, not just for the tunnel encryption and to prevent snooping. Deciding on a VPN is pretty complex. For more advanced usage, I recommend you setup your VPN on your home router and this saves you a lot of time instead of configuring it on every single device. Your VPN server is going ot have a hiccup every now and then having to restart your VPN client on every device is really annoying.

There's a number of aftermarket firmware like the asus merlin firmware which makes it easy to setup multiple VPN providers. The important thing is to setup a killswitch where if the VPN goes down, then your router should stop routing, otherwise the default is to send it over clearnet and this will happen and you won't notice for days and weeks until you don't see these "identify this street sign" captchas that you often got when you tried to login and then they stopped.

With high-end consumer routers, I have this dual CPU router over here, it maxes out at 30 megabits/second and if you want more than that you want a VPN accelerator or buy a beefy standalone linux box that you setup to be a router itself and it can do the compression and decompression a lot faster than these expensive at home routers.

## Protect yourself from your phone

Phones are really terrible for privacy, but they are really convenient. The best option is don't carry a phone. If you must have a phone, then go the prepaid route. Use cash or some anonymous form of purchasing a prepaid phone that is not a subscription plan that does not have your name or address connected to it. It can be tricky to do. I'm a big fan of The Wire, so I figured I'd be able to get a burner at any gas station. In my area, that was not the case. I asked for prepaid plans and they asked for an ID. Apparently homeland security and all that stuff. I had to go online and get a trackphone without giving identifying information.

If you're using virtual phone services like numberproxy and tossable digits... you can have a second proxy for your phone. You never give out your burner phone number, but you give out burner virtual numbers that forward to your burner phone. You protect yourself even more by doing this, and it should protect you from SIM swapping. If someone finds a phone number associated with you, they don't know which service to go to to try to social engineer to steal your phone number.

## Other online account protection

The only password you should know is the password to unlock the password manager, which you should be securing with hardware two-factor authentication. All of your passwords should be long and complex. Emails are a big point of failure. You should always use hardware 2FA. Don't reuse passwords. Everything that goes into a database on the internet will eventually get compromised.

If you're not a yubikey fan, then trezor can be used as UAF.

## Protect your communications

Signal and telegram offer some options for protecting your communication. Cisco has a registered encrypted email service. Sendsafely sends encrypted files. I don't have PGP on this slide. I can count on one hand the number of people I can contact with PGP encrypted emails, and it's just way too difficult for the average user and you shouldn't expect people to know how to use PGP.

## Protect your financial data

There's a lot of credit reporting agencies. If they get hacked, then your identity can get stolen. You should go to every one of these and request a security freeze.

## Protect your purchases

Cash is king for buying stuff. But a lot of places don't have the right cash on hand to give me the right change. The next best thing is prepaid debit cards. You can also get a number of different virtual prepaid debit card services; privacy.com is an interesting one because they leyt you create an unlimited number of cards with spending policies and burner cards. Downside is that this hooks up to your checking account; but you can use an anonymous LLC or another entity, setup a checking account with them, then setup privacy.com to your anonymous checking account. This works, it takes a few days for them to approve it, but I haven't had any problems with this.

You'll run into some issues with these services because some merchants don't accept debit cards.

## Protect your driver's license

We hae ot provide multiple proofs of residence to get a driver's license in the US. If you find yourself in this situation, then you can't prove your residence if you have done the other steps in this presentation. You might have to go to a friend, or find some cheap room or apartment or RV lot because you have to get utility bills and bank statements at that address to prove that you live there.

In terms of general leakage prevention, because there are places that ask you for your ID, you can get a passport card hwich will not have an address on it or a state that you live in.

## Protect your vehicle

There are some products you can get but they might be legal or illegal in some jurisdictions. If you have a car owned by an anonymous LLC, that's probably the best thing to do. A lot of these newer cars have tracking services built into them; you might want to disable those. You might want to get an older vehicle or a cheaper one that doesn't have that. I've found I've been able to use anonymous LLCs to setup accounts with p2p ridesharing services. I can use Uber and Lyft without having my identity associated with those accounts and thus not have my movements tracked.

## Protecting your data at national borders

There's a few schools of thought here. One is carry your data with you and encrypt it, or another is don't carry any data at all. How are you really going to get the data on the other side? You could mail an encrypted drive to your desitnation; you could have it hosted on a secure server which you download later but hopefully there's enough bandwidth... or use your client as a thin client and remote into a remote server.

## Stretch goal: Misdirection

If you want a challenge phase, try misdirection. When you're getting ready to move, talk to various people and tell them you're moving to somewhere you're not. You could even make a trip out of it, check out a location, check out some apartments, open a small bank account that wont cost you very much, get a ping on your credit report that you're setting up in that area before you lockdown your credit. What you're trying to do is cost it more resources for someone to find you. By sending them down the wrong path, hopefully they will realize you're screwing with them.

## Stress testing

The only way you know this works if someone can find you. So I have hired private investigators and whitehat hacker to try to track me down. I thought my driver's license would not be a big deal. The majority of states in the US have been selling driver's license data for decades at this point. Also, you could do social engineering on your friends and family. These are the weak points. Also, the people you work with to setup your privacy like bankers and lawyers. Pretty much everyone has no clue how to do this stuff and they are going to make mistakes. You could ask them to only use VPNs and encrypted channels and they will probably submit things unencrypted, so you have to watch your back and watch everyone else you're working with.


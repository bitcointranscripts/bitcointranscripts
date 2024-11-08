---
title: Bitcoin Custody
transcript_by: Bryan Bishop
tags:
  - regulation
speakers:
  - Bryan Bishop
date: 2018-09-23
media: https://www.youtube.com/watch?v=D2WXxgZ8h-0&t=22160s
---
<https://twitter.com/kanzure/status/1048014038179823617>

Start time:  6:09:50

My name is Bryan Bishop, I’m going to be talking about bitcoin custody. Here is my PGP fingerprint, we should be doing that. So who am I, I have a software development background, I don’t just type transcripts. I’m actually no longer at LedgerX as of Friday (Sept 21 2018) when I came here.  That is the end of 4 years, so you are looking at a free man. [Applause] Thank you.

So what is custody? A few of these slides will be about regulations and custody. According to the SEC and the code of federal regulation 17 CFR Part 275. The custody rule is really misnamed. The custody rule is that it is forbidden for you to have custody of assets. So the custody rule is that that you can’t have custody. Custody is defined as things like possession, access, authorization, and legal ownership, other things like that.

So all of these things have to be avoided in certain situations according to the securities regulator in the United States.  This is contrary to bitcoin though, because in bitcoin basically third parties are designed to be security holes and you shouldn’t use them. Verses the intent of the custody rule or at least one of the intents is that it is about reporting and requirements around things like, you don’t want the person managing your funds to steal all the money so you have to go with qualified custodian which are defined as banks, future commission merchants, broker dealers, or ambiguously foreign financial institutions. But with bitcoin you can say here is the public key and we are going to keep segregated accounts and maybe it is bip32 or something and this seems like a more secure way of doing custody and storage especially for buy and hold scenarios, which under the regulations if you go work with someone in a fund who is just doing buy and hold it has to be a qualified custodian but in my opinion it could be considered a third party security hole.

So for regulation in particular while it is a wonderful idea to say just work around the regulators and don’t do any of that, it would also be good to give them realistic advice on how bitcoin works and make good proposals and good faith attempts to to tell them how bitcoin works and what they should be requiring. This often means you should give actual examples to regulators about how things work, don’t just say use multisig.

I recently drafted with a few co-authors a letter to the sec about bitcoin etfs and things like
encouraging them to use public auditing with public keys or even things like secure ways of transferring bitcoin to the investors if they want to redeem their bitcoin holdings from the etf.

At LedgerX I was a full stack developer and also their bitcoin expert. I helped them design their bitcoin custody solution and a number of other things.  They are regulated by the CFTC, they run a bitcoin clearinghouse and bitcoin options exchange, things like that.  Really quickly lessons learned from this is, automation is really good but sometimes it is not necessary. You can spend a lot of time and resources and costs developing software automation, but often it is better to manually do bitcoin transactions, especially in this case because their withdrawal process is very specific and it is not high volume in terms of the amount of data going through it.

Also there is no end to end off the shelf hardware security solution. I’ll talk about that a bit more in a few minutes. We actually know a lot about this, this is just ways to store bitcoin.

So when you are designing a way to store bitcoin either for yourself or for a company you have to think about what is appropriate. This is based on what type of threats you have to protect against and you also have to be really be really clear on how it works. Probably no one in your family will know how to recover your bitcoin when you die.  So that is a really serious problem.

The way to fix this and the way to do this in companies is just a lot of checklists and documentation. Can’t have enough checklists. Maybe at the end when you have 20 pages of checklists, one of the checkboxes can be to remove some checkboxes, but not until then.
In particularly for companies that are storing bitcoin I recommend a signing ritual or signing ceremony. Signing ritual is a defined process that is well documented with checklists, possibly with video surveillance and this is things like accessing the hardware security module or the hardware wallets or combining the hardware wallets or separately going to the hardware wallets in different venues and locations.  And having an actual process and training around this. And you will probably have to train the non technical members of either your company or family or whoever you are working with to actually be able to do this. One public example that is probably the most elaborate public example of a signing ceremony is a DNSSEC key signing ceremony.  Someone else also mentioned to me that Verisign had a really early key signing ceremony and they were even using vhs tape to record the whole thing back in the day. And they even had transfer procedures specifically for handling the tape. But that was not public. This is probably the most public one you will see. It’s like 4 hours of ritual and you can watch it, the most exciting thing you will ever see on the internet.

If you were to build out to store bitcoin there are three main topics to look at. One is risks, what happen to key material, what will happen in the world of bitcoin you should consider all of these and write them out. There is also a threat model- what are the adversaries trying to protect against. Some things you can’t defend against, like nation state actors, but you can probably defend against lesser skilled adversaries and petty thieves.

If you are choosing to use a third party for any reason related to bitcoin even it is an escrow agent, or someone on two or three multisig, or even if they are coinbase.com where they have entire control of your biticon, you need to ask who are they, who is working for them, what are their experiences, are they qualified. I’ve often asked companies do you have an bitcoin developers at all and they often say no, but they claim to be a bitcoin company, so how do they know how the systems works if they don’t actually have the talent inside the company.

Then want to put together custody into something you can use. We talked a lot about hardware wallets, not going to repeat this much, expect for screens. Hardware wallets should have screens on them, this is very helpful, what is hardware device about to sign if you allow it to sign.

There is also a segment of the market called hardware security modules, but I think it is a false way to dissect the market or outline the market.  It should really be the same hardware for both market segments. Furthermore there is further advancement of hardware wallets which is either for exchanges or even for personal use like lightning nodes, you want to have a hardware wallet that can quickly sign off, especially if able to prove it strictly increases personal balances. That are  transactions you should usually be ok with it, It is useful for lightening, conjoin and other purposes. Another way to have hardware wallets is something I call a cryptographic multisig
like non bitcoin multisig. Can have signing ritual process instead of logging into your hardware wallet perhaps you have other cryptographic hardware devices required to access that device and this is an additional layer of security on top of bitcoin multisig.

Now into some technical details, partially signed bitcoin transactions I talked about that earlier today on a panel, just a serialization format, but makes it easier to transfer data from bitcoin wallets to hardware devices.

It is bip 174 I believe is already implemented and merged into bitcoin core. Pre signed transactions are an interesting technique. This is the concept where if have an elaborate process where have to fly around the world to access your bitcoin consider making per signed transactions at the same time. If sending money somewhere as part of maintenance of finances can also sign transactions don’t intend to send.except under certain circumstance and you can encrypt those and store those somewhere safe. You can encrypt those and store somewhere safe. In the event that you lose access to your hardware or the end of the world occurs, you can send the pre signed transactions for whatever purpose.  Another method similar to that is a way of enforcing a similar system to bitcoin vaults. And this an idea where you send bitcoin to an address and then with the private key for that address which you specially create for this purpose you sign a transaction that has a time lock sending it to another address, then you delete that private key so it only signs one bitcoin transaction in its entire lifetime. And this ensures time lock will be enforced. Adversaries can’t get the key if it is deleted.

I think we should tell regulators that everyone should be using hardware wallets or using hardware wallets. It is generally good thing to tell people to do. Although interestingly enough in the bitcoin space, a lot to the early entrepreneurs were just crazy risk tolerant so they got into bitcoin which is really risky, then started companies which is also risky, and were very happy to ignore regulators which is another layer of risk, so should be very careful which companies you deal with and figure out what they are actually doing.

And this is an idea I came up with it is not particularly novel, in one of my earlier slides talked about if not allowed to have custody of bitcoin if trading it or storing it even under guise of financial purpose beyond 150 million USD, this idea is that instead of holding the money you have the investors or bitcoin holders keep it on their machines, then you send instructions to their machines and they can chose to sign off on such as trades. It turns out there is actually a company regulated by SEC called New Wave. New Wave kind of does this except they hold everything themselves. They might not even need to use technology like this.

Another interesting thing going on is, Christopher Allen and I and a few others are putting on together a smart custody workshop in San Francisco where we will talk about all these issues and analyze specific examples of custody risks and threats and risks and wallet, and also show how to use hardware wallets. If interested can go to smartcustody.com

It is mostly for offices and people managing large amounts of money, so either go to the website or email us.  We should have custody products off the shelf, I don’t mean just hardware but training and video documentation and have people to fly out to put together. It is not enough to hand a hardware wallet, it needs to be a complete training solution and that is all that I have.

End time: 6:23:21

Do I have time for questions.

Questions follow.

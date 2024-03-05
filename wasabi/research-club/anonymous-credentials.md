---
title: "Anonymous Credentials"
transcript_by: markon1-a via review.btctranscripts.com
media: https://www.youtube.com/watch?v=pgErjQSQQsg
tags: ["research","privacy-enhancements","cryptography","bls-signatures"]
speakers: ["Jonas Nick","Max","Lucas","Rafael","Yahia"]
categories: ["club"]
date: 2020-04-14
---
## Introduction to credentials. / Selective signing of attributes. / Range proof. / "Rethinking Public Key Infrastructures and Digital Certificates" (Stefan Brands, 1999)

Jonas  0:00  
To approach this is to look from the point of view of blind signatures, right? I guess blind signatures are mostly familiar to this audience, right?

Unknown speaker  0:14  
 Yes.

Jonas  0:17  
Or should be familiar for every Wasabi Power User, I guess. So the idea of credentials is similar in the sense that you get some blinded token that was signed by some server and the server does not see the message that was being signed. Now, the additional idea to a credential is that it's not only a message that is being signed, but instead, it's multiple attributes that can be signed. And these attributes can be anything. The interesting thing is that you can selectively reveal these attributes, you can say, here I have a token. And in this token there is this attribute, and it has this value. So the not standard example is you have a token from your government, let's say, and let's say birthdate is one attributes and then assigned. Now what you can do with that you can not only show your attributes, you can also show that it's in a certain range, you can do a range proof. So what you will do is if you go to the cinema, you don't have to reveal your age, you don't have to reveal anything else that is included in your credential, you only have to show that you are older than 18 years. And that works with such a credential. And these attributes are pretty flexible. You can for example, besides range proofs, you can show that if you have to blinded tokens that attributes are the same, for example. Yeah. So mathematically, I think the best way to think about this is as Peterson multi commitments. So in normal Peterson commitments, right, you have some randomness, and you use that to commit to a value. And you basically have two different group generators. Now with these multi commitments use in some of these credential approaches, you have randomness, and now you commit to multiple attributes and only a single one. And usually you have as many generators as they have attributes. So I think historically, one of the first notions of these credentials was by Brands, I think Peter Brands, not quite sure. He wrote his PhD. Yeah?

## Pedersen multi-commitments.

Unknown speaker  3:19  
Stefano, I think, not Peter, or something like that.

Jonas  3:Unknown speaker5  
Okay. Brands is his last name. He wrote a PhD thesis about his idea of doing credentials, and it's actually quite interesting, I can recommend it. It's not too technical. And he has a lot more ideas than just credentials. But one problem with it was that so far, every attempt at proving it secure in the random oracle model failed. And this is where this anonymous credentials light paper comes in, because they have a construction that is provably secure. And if you can do basically the same things, or very similar things as with Brands credentials. There might be one minor problem. Last time I looked at it I did not really solve because in the paper, they say for 1Unknown speaker8 bits security, we recommend using a group of 576 bits. And, of course, our sector group is only Unknown speaker56 bits. So it's not sure if you can use that. It's often the case that due to the proof, these groups need to be much larger than they are used in practice even for snore signatures. Our SECP group would actually be too small 1Unknown speaker8 bit security, mostly people say, yeah, that's just an artifact of the proof doesn't really matter that much. But in order to verify that we would need to look into the proof more closely. Yeah.

Unknown speaker  5:Unknown speaker6  
Thank you. Did you finish?

Jonas  5:31  
Yeah, that's almost everything I wanted to say. Like, the other thing I wanted to say is that these tokens are pretty flexible compared to just Schnorr signatures. So at the building on Bitcoin Conference, Unknown speaker018, I talked about how to use this to basically swap a token that is in or that is most created with an anonymous credential with an on chain or off chain Bitcoin on lightning without the server knowing that this happened and without having to trust the other party.

## Improvement on Brands' credentials.

Speaker 1  6:10  
Yeah, thank you. I'd like to point out so we are reviewing right now, paper card anonymous credential slight and as Jonas pointed out, this is an improvement on the Brand's credentials. In fact, it has one difference between the Brand's credentials. Well, this is more secure, of course, because the Brand's credentials couldn't be proven. But actually, these tokens are linkable with each other. So, if you have a credential, you can create as many blind signatures for it. And you can prove that credential as many times as you want, unlike the brand credentials, because they're the linkable. So you can only use up to as much signatures as much the designer allows you in our case, would be the coordinator. So that's actually something that we would desire if we would want to build on top of this enemy.

Jonas  7:Unknown speaker8  
If I may add to that, I would say that Brands credentials are also on unlinkable if you can talk to the server, right? Because that's what you also usually do in e-cash, you basically show the serial number of your old token, you create a new token, you show that the tokens are the same in zero knowledge, and then you get a signature on the new token. And that way, you get unlinkable token. I think the advantage with Anonymous credentials slight is that you can do that without having to talk to the server.

## Mercurial signatures (Crites, Lysyanskaya, Unknown speaker0Unknown speaker0). / Delegatable Anonymous Credentials.

Speaker 1  8:03  
Yes, it's called I think, reissuance or that's what usually comes up. Anyway. So a bit more there. Because the same outdoors were working on this for probably a decade of this paper and, and they actually came up with something called mercury, our signatures where they don't need so much crypto as much as in this paper. But what in a very straightforward way they could achieve the exact same thing with this mercury as signatures. And even more. They were working on some things called delegated anonimous credentials, and they're the three keys that you could actually delegate the ownership of the credential to someone else. So in our case, that would be I think, giving money to someone, and I wouldn't be able to redeem it, but you would, which is actually pretty nice. Oh, my God, I wasn't talking?

Jonas  9:Unknown speaker5  
Last thing you said was in our case, that would be.

## Rationale for using blind signatures for Coinjoin.

Unknown speaker  9:31  
Yeah, it's interesting, because I think it's recording everything that I'm saying but you didn't hear. So I think what you said is, in our case, well pay someone in a coin during round without us being able to redeem it but that someone would be able to redeem it as an output of the coin chain. I just wanted to point out that Dell tours were actually working on this line of research for a long time, and they think they came up with much better constructions and easier ones, too. So if someone would like to look into these anonymous credentials, and definitely look into the newer stuff, there. Okay, so far any comment here? Because I want to approach it also, from a coin join point of view that why did we, why did we wanted to use it, and why we don't want to use it anymore. So, in the problem that we are trying to solve is to be able to have some kind of divisible e-cash system actually, that allows us to come with any input in anonymity network identity, and then we get back some credit for that input. And, if we come with another input later, then we get back some credit. And then somehow we can combine those credits and come with only one output, or we could also break those credits down. And with the stupid blind signature scheme, we will have to create a bunch of denominations and a bunch of signatures survived this paper would be handy here because we still need to create the bunch of denominations. But we wouldn't need to create a bunch of signatures, the user could create the signatures, the blind signatures for their credentials. Later, however, we actually came up with the solution based on homomorphic cryptography commitments, range proofs, and buying a blind signature scheme that works with this homomorphic cryptographic commitments in a way that we can actually come with an anonymity network identity, register input, get back something, come with another anonymity network identity, register another input, get back something. And we could combine that to something in zero knowledge that in a way that we could prove the server that we could make any kind of outputs out of those. And we could have done it with these anonymous credentials in some way or form. But we would still had to have denominations in order to achieve some kind of privacy, that was the sort of line there, right? Jonas.

Jonas  13:34  
Just so I understand instead of registering all inputs at once, you would be able to register them with different identities, right?

Unknown speaker  13:47  
Yes, we can come with different identities with any number of inputs and we can come up with different identities to register any output that's what we care about.

Jonas  14:06  
So you would provide a let's say, one bitcoin input and another one bitcoin input later and then you would get two one input one bitcoin tokens, and that could be used to add a two bitcoin output or something like that. And you don't have to show that your inputs were one Bitcoin you just show that the sum is equal to two bitcoins. Yes.

## Explanation of breaking inputs, merging commitments.

Unknown speaker  14:35  
Yes. In fact, even more we can merge them and break them down in any way of shape or form. Because this this session is about anonymous credentials and I will bring up some topics but yeah, I will risk to explaining it to you because it's really interesting. And I think it's really no one number. You can think about it, the breaking part is easy. And I think that that you understand it easily. And I can explain it to you. Because if you have one bitcoin, and you want to pay 0.1 bitcoin to someone, then it would be like this. You create two powders and let's say powders and commitments to 0.1 bitcoin and to 0.9 bitcoin. Those will be your outputs in the coin joinm, right? So for it's clear.

Jonas  15:49  
Yeah. 

Unknown speaker  15:50  
And then you register that two pedders and commitment for your one bitcoin input. And you of course, tell the coordinator that hey, this one bitcoin input, I'm going to prove that it is mine. And this is the sum of my podders and commitments. By the way, we create more powders and commitments with zeros, but it doesn't matter for now. 

Jonas  16:31  
Yeah. That makes sense. 

Unknown speaker  16:3Unknown speaker  
Yeah. And then, we also found the blind signature scheme that works with pedders and commitments. So the coordinator can give us something from what we can create a signature own, or values, which is cool, because then we can just come at output registration, that, hey, I'm registering the 0.1 bitcoin output, and I have a signature on it. And with another anonymity, network identity, hey, I'm registering the 0.9 bitcoin output, and I have a signature on it. So this is the breaking part. And the merging part is different because we couldn't figure out with pedders and commitments range proofs. And, yeah, of course, there needs to be range proof, along with the pedders and commitment, but I think that's obvious. Anyway, we couldn't figure it out with the blind signature scheme on pedders and commitment, but we actually had to use BLS signatures. And with that, we could figure out how to merge together more than one commitment. Yeah, so it's pretty cool. Yeah, any question on that or we can get back to this paper?

Jonas  18:10  
Yeah, I don't quite understand why that wouldn't work. Let's say have a point one and a point nine bitcoin token, right? 

Unknown speaker  18:Unknown speakerUnknown speaker  
Yes.

Jonas  18:Unknown speaker4  
 Don't you just have to show to the server that both tokens sum up, or maybe even better you create a new token with a one bitcoin value. You don't show the server the value of the new token, and but you show the server, that the sum of the old tokens is the value of the new token. Wouldn't that work? For lodging,

Unknown speaker  18:5Unknown speaker  
Your first suggestion. Yes, that works. It's just there is some probably negligible of privacy loss, right? Like you expose the server that you have 0.1 bitcoin and 0.9 bitcoin, pedders and commitments and the share.

Jonas  19:13  
At least with anonymous credential slide, I don't think you have to do that necessarily. I think you can show that the sum is the value of your new token and you don't have to show anything more to the server I think.

Unknown speaker  19:3Unknown speaker  
With your first suggestion, I was talking about that, right.

Jonas  19:37  
 Okay.

Unknown speaker  19:38  
That's not a huge privacy thing. So it can work. But we figured out how to do it even without that. So your second suggestion could you repeat it maybe? I'm not sure I understood.

Jonas  19:56  
I thought I was only making one suggestion and so perhaps I'm not sure what the second one would be.

## Reissuance of tokens.

Unknown speaker  Unknown speaker0:05  
So your first suggestion was to take two blind signature of 0.1 and 0.9 and register them tog to the coordinator, is that correct?

Jonas  Unknown speaker0:Unknown speaker4  
Perhaps I wouldn't call this registering, I would just call this like, perhaps like just the reissuance, we've used that term before you have a token, and you will just want to get a new one with a new serial number. And these tokens are unlinkable. And the same would work if you show two tokens. And a new token where the new token is the sum of the former tokens, and you don't have to show the actual values to the server, you just have to show that the sum matches to the new value. And then you wouldn't have the privacy loss of having to show the individual values of the old tokens.

Unknown speaker  Unknown speaker1:11  
Yes, so the thing is, we get the blind the signature on the data itself, which means if we want a reissuance phase there, then we will have to expose the values. 

Jonas  Unknown speaker1:33  
Okay.

## Are denominations required by anonymous credentials?

Unknown speaker  Unknown speaker1:34  
 So, there might be some scheme that works with the with BLS signature, we actually figured it out how to do that, because they're the signatures actually has the message itself. So it's really fresh, I just learned about it today. And something like that you can give the two blinded BLS signature to the coordinator and prove that their sum is this value. And because of the blind BLS signatures are the unique tokens there, this way, we won't have problems. So with anonymous credentials, I think you would have to, to create a bunch of bunch of denominations, right?

Jonas  Unknown speakerUnknown speaker:46  
I don't think so. I think this is exactly the magic of these anonymous credentials that you can do these. Some proofs. Similar to what you just described with the BLS signatures.

Unknown speaker  Unknown speaker3:03  
That's really similar with what we came up with indeed, but I'm not sure in this paper. Maybe I just didn't go into it.

Jonas  Unknown speaker3:Unknown speaker1  
If I remember correctly, perhaps they're not showing this in this paper. But this is something that is like a central concept in the Brand's PhD thesis. I believe you can do the same thing with anonymous credentials, because both types of credentials look actually very similar.

Unknown speaker  Unknown speaker3:5Unknown speaker  
All right. Would it make sense to start investigating this instead of doing it with BLS signatures?

## Anonymous credentials vs BLS signatures

Jonas  Unknown speaker4:08  
Actually, I think I don't know. I will do whatever is easiest, actually. Because I guess for your application, or in general, it doesn't make too big of a difference. If you use BLS. I mean, if you think that parents are secure and BLS signatures are secure, and this whole bunch of crypto sanctions that I think you can just use that if that's easier. I don't think you have to restrict yourself to something that works in the discrete logarithm paradigm.

Unknown speaker  Unknown speaker4:46  
Aren't BLS signatures work on the discrete logarithm paradigm?

Jonas  Unknown speaker4:50  
No, they use pairings. So it's different curves and different crypto assumptions.

Unknown speaker  Unknown speaker4:59  
Okay. All right. So yeah, I'm not sure it is easier for us because the implementation since ours, I think still lacking behind of the BLS signature implementations. So, on the other hand it's such a simple scheme that even they could even explain it to me who doesn't understand crypto that much.

Jonas  Unknown speaker5:30  
The BLS thing doesn't have an implementation. And if so, how is it called? So I can find it?

Unknown speaker  Unknown speaker5:37  
I think it does not have implementation in C. It has for a couple of languages. I think the main implementation is C++. And there is bindings for that.

Jonas  Unknown speaker5:54  
I think there's an implementation of Brands credentials in C, right. That's see your proof library.

Unknown speaker  Unknown speaker6:01  
Yes, I was playing around with that. In fact, I ported it to dotnet core. And it's not that obvious how to use that. But the code is very clean, and very nice. So I would have loved to go with your proof.

## Problem's with proof. / Brands' credentials.

Jonas  Unknown speaker6:Unknown speaker1  
Well, what's the problem with your proof?

Unknown speaker  Unknown speaker6:Unknown speaker6  
Well, that doesn't solve our problem. As far as I understand it, you do need a bunch of stuff. To deal with that. Also, people are talking about that it's not very secure, and things like that.

Jonas  Unknown speaker6:47  
No one's found in vulnerability yet. Brands credential. So as far as I know. I know, it's a difficult question. But I think the the sum proof that I mentioned earlier, should work just as well with Brands credentials, you don't need multiple denominations.

Unknown speaker  Unknown speaker7:14  
Because Brands credentials would be able to prove the sum. So how would the range proofs apply to that?

Jonas  Unknown speaker7:34  
Yeah, you probably still have to do this range proofs to show that the values don't overflow. But I am not sure if the you prove library does that already for you? And really looked into the library?

Unknown speaker  Unknown speaker7:48  
How about the merging of the coins? I think that could be a problem there that you cannot merge two attributes together in a way that it both prevents double spending. And and you don't expose the attribute, you know, the values only the some of them? I'm not sure that's possible?

Jonas  Unknown speaker8:Unknown speaker9  
I think it is. I think that's the point of Brand's credential. If you do a reissuance, you don't have to show all the attributes. You prove to the server that your new token doesn't have any other value than the sum of your old tokens combined. I think and this is possible with Brands credentials.

Unknown speaker  Unknown speaker9:00  
You don't need a ressuarence there.

Jonas  Unknown speaker9:04  
Yeah, you wouldn't need the reissuance.

Unknown speaker  Unknown speaker9:07  
Finally, there is an argument why our scheme is better. Because we don't need reissuance scheme there.

Jonas  Unknown speaker9:Unknown speaker3  
That sounds like something that BLS or parents could do. Like merging different credentials together without communication with the server, so nice to me that sounds plausible.

## Unlinkable re-use of credentials.

Unknown speaker  Unknown speaker9:40  
I 'm just going to read a few things about here is that you prove from the the article that to be for everyone knows what we're talking about. From the efficiency point of view. Therefore, the you prove credential system based on Brands work acquired and implemented by Microsoft seem attractive, you prove does not allow unlinkable reuse of credentials in order to unlink ability, use a credential again, in order to unlinkable user credential again, a user must get it re issued. Which actually suggests that, in fact that this paper doesn't have linkable credentials, only unlinkable one. These lines don't suggest that, but that's what's in the paper. Let me see one more thing there. When such proof is carried out, it cannot be linked to previous users of the same credential, or any other identifying information about the user. Is what I what I'm talking about here, we actually want the opposite. In order to avoid the worst spending, we want a use to be linked to previous users of the same credential. Which brands provide and this scheme does not? I'm not sure how hard would it be to to implement it? Would it be only a simplification, or this would be a major headache to implement linkable credentials on top of ESEA construct?

Jonas  Unknown speaker:10  
On top of what construct?

Unknown speaker  Unknown speaker:14  
It's like the speaker's anonymous credentials like ACR?

Jonas  Unknown speaker:19  
Yeah, I think that's easy, because one of the attributes would just be the serial number that the server stores, I mean, the service does have the serial numbers, of course that have been used, right? You wouldn't need the ratio once again to show your serial number, and then you get a new token.

Unknown speaker  Unknown speaker:45  
That would also ruin the sum stuff that we talked about with.

Jonas  Unknown speaker:53  
No why?

Unknown speaker  Unknown speaker:53  
If you put a serial number into the attribute, then you cannot prove the sum. I mean, the serial number is there, you know.

Jonas  3:09  
So what you do is, you show your old credentials can be multiple, you show the serial numbers for each of those credentials, you prove that the serial numbers are actually the ones contained in your credentials, the server checks that the serial numbers have not been used. Your show the new token, that you created with a fresh serial number, serial number that you chose randomly. And then you do the sum proof. That way, you don't have to show anything to the server, but the serial numbers.

Unknown speaker  3:49  
I don't know. 

Jonas  4:07  
Yeah, the problem is with blind signatures, right? As you blind signatures as unstructured, you just have this message and then you can put different things into the message, but then you cannot efficiently prove anything about these individual attributes in your message. And this is why these credential schemes are superior to the normal blind signatures.

Unknown speaker  4:30  
There may be something here, too.

Jonas  4:44  
Yeah, I'd also like to look into this BLS stuff. Definitely that seems interesting.

Unknown speaker  4:5Unknown speaker  
I'm going to link the repository in the comment here, but don't share it yet because we did not figure out the name and we have a stupid name for now. 

Jonas  5:17  
Okay. I see it. 

Unknown speaker  5:Unknown speaker1  
Do you guys have anything to ask or talk about regarding anything maybe? Everyone is really silent. Go ahead, Lucas.

Lucas  5:48  
No, I have no question because I am not either know this primitives yet. I have to study a bit more.

## E-cash.

Jonas  6:05  
I learned most of that from Adam Beck he wants gave a presentation about brands credentials at Block Stream. I learned a lot from him. But that wasn't public unfortunately. I think I have the slides, but I don't think they're very helpful. So perhaps the best starting point is still Brands PhD thesis, it's very long, but just have to check out some parts of it, I think. Because especially the things like this anonymous credential slide, there seems to be like the difficult thing about or to grasp about it is not I mean, this scheme exists. But the question is, how do you use it? And how do you use it with serial numbers and to get E-cash tokens with multiple denominations, right? That's not in the anonymous credentials, light paper. That's something that Brands talks a little bit more about.

Unknown speaker  7:07  
Even more, because, as we reviewed this paper, and we looked into that, well, how could we use it for E-cash kind of stuff, then we just stumbled upon a tremendous amount of literature there. That's how to do divisibility cash systems, and three, like, a couple of 100 of paper is going on on this issue. But the thing is, they are solving things that we don't need to solve because CoinJoin sorry, inherently secure. If someone doesn't see their outputs then it's not going to sign. And that's up here. So our job is basically to simplify what they have.

Jonas  8:04  
Right? There's also the concept of offline E-cash, which also doesn't seem to be very practical in the bitcoin world. Because in offline E-cash, if you double spend, you reveal your secret key, which perhaps as if you're an attacker, that's not a big problem to you, because you already have your bitcoins. So you don't care about the secret keys in your token, you have twice as many bitcoins as you would have normally. So they don't seem to apply.

Unknown speaker  8:35  
Yeah, that's not even a requirement here. Because everyone is online. In fact, even all the participants are online, although you're not.

## Next steps.

Jonas  8:48  
This idea of merging inputs and so on. That's really interesting, I think.

Unknown speaker  8:55  
We are going to work on that and either look into that issue, that's where we figured out how things should be. But we are going to create a draft and send it to the bitcoin dev mailing list then and things like that. And also for the next Wasabi Research Club each one is going to write down exactly this scheme, the cryptography part of it. That's what I would like to propose for the next Wasavi Research Club, because as we looked through E-cash papers and anonymous credential papers and every kind of papers it looks like this is the simplest and most straightforward solution for really arbitrary coin joins, which we are not going to do but we would like to have that flexibility and that's what lets us improve upon it in the future. Max asked, what about farewell decided equal value outputs? Anyone understands the question?

Jonas  10:Unknown speaker1  
 No. 

Unknown speaker  10:Unknown speaker5  
All right, sorry, Max. We can't reply you. One more interesting thing is that. Max figured out that for tiny one of the author of this paper we are talking about actually had some involvement in tamber bit. I'm not sure exactly what but she was doing something tamber bit.

Jonas  10:56  
If no one would like to say anything, because this was quite a difficult paper, then we can cut this short, unlike other conversations and we can we can go. Do you guys have anything else you would like to talk about?

Rafael  11:31  
Not yet ready. I'm just fascinated about things that you guys talked about.

Jonas  11:40  
I talked about almost everything I know about it. So let me know how this progresses. And what do you find out?

Unknown speaker  11:5Unknown speaker  
Yeah, definitely. We are going to talk about our scheme in the next Wasabi Research Club. If no one has an objection  or alternatively, we could review Adam Gibbs from zero knowledge to bullet proofs paper, I think that could be useful, or our scheme which might make more sense, to be honest. But it could change. Maybe we figure out how there is something utterly wrong with this and then next week would be would be pointless. But I doubt at this point, we really reviewed a lot of things last week. Should the next generation Wasabi mixing technology be the topic of the next Wasabi Research Club? What do you guys think?

## Equal value denominations.

Rafael  13:09  
I think it's good. But there was a question from Max. And that is the difference of users who want to be a part of the equal value denomination and those who want only specific amounts?

Unknown speaker  13:Unknown speaker4  
Yeah, no, there is no difference. It's equal value denominations, as I imagine it right now or we did not work this out at all. But I think that could be something that the users create by themselves. So if I participate in a mix, then I'm going to parties I'm going to ask for outputs of some standard denominations that I guess, I estimate other users, I suspect other users are going to do too. But I could create outputs in any way shape, or form up to the maximum limits, of course, as I would like to even do a pay to endpoint transaction in a coin join, which would be neat. 

Rafael  14:Unknown speaker6  
It sounds good.

Unknown speaker  14:Unknown speaker9  
 As a really interesting thing, we just had a talk with doge. Not going pronounce it. One of the guy who came up with the Lightning Network and he actually came up with the coin swap protocol. There is still some denial of service issues he didn't figure out, but he came up with the coinswap protocol that after top priorities in snore, and priorities in bitcoin. And then he could do coinswaps those could be completely unnoticeable. That's really exciting. I just wanted to share this fresh information. Thank you guys, and sorry for this unconventional Wasabi Research Club now. Usually Aviv does a very good job at explaining the concept at the beginning but he couldn't make it last minute. So no one could really prepare but Nick gave a great summary of the paper.

## End.

Rafael  16:04  
Absolutely. You guys did a good job. Thanks for that.

Unknown speaker  16:10  
Yes, thank you Nick. And thank you for inviting this special guest.

Jonas  16:15  
What an honor.

Unknown speaker  16:Unknown speaker1  
I guess that's it. Like, share and subscribe. Bye bye.

Jonas  16:33  
 Bye, everyone.

Lucas  16:33  
Bye, guys.

Rafael  16:34  
Bye.


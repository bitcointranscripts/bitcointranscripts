---
title: Anonymous Credentials
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=pgErjQSQQsg
tags:
  - research
  - privacy-enhancements
  - cryptography
  - bls-signatures
speakers:
  - Jonas Nick
date: 2020-04-14
summary: Jonas Nick discusses anonymous credentials and their applications in this section. Anonymous credentials involve getting a blinded token signed by a server, where the server does not see the message being signed. These tokens contain attributes that can be selectively revealed, and range proofs can be used to verify attributes without revealing additional information. The speaker highlights the flexibility and security of anonymous credentials and how they improve on traditional signatures. They also discuss advancements in these credentials, such as mercurial signatures and delegateable anonymous credentials. The speaker mentions the work of Del Tauri and their solution for creating a divisible e-cash system using homomorphic cryptographic commitments, range proofs, and blind signature schemes. They also discuss the merging and breaking of anonymous credentials, as well as reissuing tokens without exposing the individual values. The implementation and linkability of credentials are also explored in the conversation. Overall, the participants express the need for further study and propose focusing on the cryptography part of the scheme in the next session.
aliases:
  - /wasabi/research-club/anonymous-credentials/
---
## Introduction to credentials. / Selective signing of attributes. / Range proof. / "Rethinking Public Key Infrastructures and Digital Certificates" (Stefan Brands, 1999)

Speaker 0: 00:00:00

To approach this is to look from the point of view of blind signatures.
Right?
I guess blind signatures are mostly familiar to this audience, right?
Yes.
Or should be.
Should be familiar for every Wasabi user.
For every Wasabi power user, I guess.
So, the idea of credentials is similar in the sense that you get some blinded token that was signed by some server and the server does not see the message that was being signed.
Now the additional idea to a credential is that it's not only a message that it's being signed, but instead it's multiple attributes that can be signed.
And these attributes can be anything.
And Now the interesting thing is that you can selectively reveal these attributes.
You can say here I have a token and in this token there is this attribute and it has this value.
So the standard example is you have a token from your government, let's say, and it says your age, basically your, let's say birth date is one attribute, and that is signed.
Now, what you can do with that, you can not only show your attribute you can also show that it's in a certain range you can do a range proof.
So what you would do is if you go to the cinema you don't have to reveal your age, you don't have to reveal anything else that is included in your credential, you only have to show that you are older than 18 years and that works with such a credential.
And these attributes are pretty flexible.
You can, for example, besides range proofs, you can show that if you have two blinded tokens, that attributes are the same, for example.

## Pedersen multi-commitments.

Speaker 0: 00:02:17

Yeah, so mathematically, I think the best way to think about this is as Peterson multi-commitments.
So in normal Peterson commitments, right, you have some randomness and you use that to commit to a value.
And you basically have two different generators, group generators.
Now with these multi-commitments used in some of these credential approaches, you have randomness and now you commit to multiple attributes, not only a single one.
And Usually you have as many generators as you have attributes.
So I think historically one of the first notions of these credentials was by Branz.
I think Peter Branz, not quite sure.
He wrote his PhD.
Yeah.

Speaker 1: 00:03:20

Stefano, I think, not Peter or something like that.
Okay.

Speaker 0: 00:03:24

He wrote his PhD thesis.
Okay, Branz is his last name.
And he wrote a PhD thesis about his idea of doing credentials.
And it's actually quite interesting.
I can recommend it.
It's not too technical.
And he has a lot more ideas than just credentials.
But one problem with it was that so far, every attempt at proving it secure in the random Oracle model failed.
And this is where this anonymous credentials light paper comes in because they have a construction that is provably secure And you can do basically the same things or very similar things as with brands credentials.
There might be one minor problem.
Last time I looked at it, I did not really solve because in the paper they say for 128-bit security, we recommend using a group of 576 bits.
And Of course, our SecP group is only 256 bits.
So it's not sure if we can use that.
It's often the case that due to the proof, these groups need to be much larger than they are used in practice.
Even for Schnorr signatures, our SecP group would actually be too small for 128-bit security.
Mostly people say, yeah, that's just an artifact of the proof, it doesn't really matter that much, but in order to verify that, we would need to look into the proof more closely.

Speaker 1: 00:05:24

Yeah.
Thank you.
Did you finish?

Speaker 0: 00:05:31

Yeah, that's almost everything I wanted to say.
Like the other thing I wanted to say is that these tokens are pretty flexible compared to just Schnorr signatures.
So at the Building on Bitcoin Conference 2018 I talked about how to use this to basically swap a token that is in or that it was created with an anonymous credential with an on-chain or off-chain Bitcoin on Lightning without the server knowing that this happened and without having to trust the other party.

## Improvement on Brands' credentials.

Speaker 1: 00:06:12

Yeah, thank you.
I'd like to point out, So we are reviewing right now a paper called Anonymous Credentials Lite and as Jonas pointed out this is an improvement on the brand's credentials.
In fact it has one difference between the brand's credentials, well this is more secure of course because the brand's credentials couldn't be proven.
But actually, these tokens are unlinkable with each other.
So if you have a credential you can create as many blind signatures for it and you can prove that credential as many times as you want.
Unlike the brand credentials because there they are linkable so you can only use up to as much signatures as much the designer allows you in our case would be the coordinator.
So that's actually something that we would desire if we would want to build on top of this.
Anyway.

Speaker 0: 00:07:28

If I may add to that, I would say that brands credentials are also unlinkable.
If you can talk to the server, right?
Because that's what you also usually do in e-cash.
You basically show the serial number of your old token.
You create a new token.
You show that the tokens are the same in zero knowledge, and then you get a signature on the new token and that way you get an unlinkable token.
I think the advantage with anonymous credentials is that you can do that without having to talk to the server.

## Mercurial signatures (Crites, Lysyanskaya, 2020). / Delegatable Anonymous Credentials.

Speaker 1: 00:08:04

Yes, it's called I think Ray Schwentz or that's what usually comes up.
Anyway, so a bit more there because the same authors were working on this for probably a decade after this paper and they actually came up with something called Mercurial Signatures where they don't need so much crypto as much as in this paper, but in a very straightforward way they could achieve the exact same thing with these mercurial signatures.
And even more, they were working on something called delegatable anonymous credentials.
And the trick is that you could actually delegate the ownership of the credential to someone else.
So in our case, that would be, I think, giving money to someone and I wouldn't be able to redeem it, but you would, which is actually pretty nice.
Oh my God, I wasn't talking.

Speaker 0: 00:09:26

Last thing you said was in our case, that would be.

Speaker 1: 00:09:31

Yeah, it's interesting because I think it's recording everything that I'm saying, but you didn't hear.
So I think what I said is, in our case it would be that we could give the, we could give, well, pay someone in a coin join round without us being able to redeem it, but that someone would be able to redeem it as an output of the coin join.
So I just wanted to point out that the authors were actually working on this line of research for a long time and they think they came up with much better constructions and easier ones too.
So, if someone would like to look into these anonymous credentials, then definitely look into the newer stuff there.
Okay, so far any comment here?

## Rationale for using blind signatures for Coinjoin.

Speaker 1: 00:10:36

Because I want to approach it also from a coin joining point of view, that why did we, why did we want to use it and why we don't want to use it anymore?
So, the problem that we are trying to solve is to be able to have some kind of divisible e-cash system actually that allows us to come with any input in an anonymity network identity and then we get back some credit for that input and if we come with another input later, then we get back some credit and then somehow we can combine those credits and came with only one output or we could also break those credits down and with a stupid blind signature scheme we would have to create a bunch of denominations and a bunch of signatures.
So why this paper would be handy here?
Because We still need to create a bunch of denominations, but we wouldn't need to create a bunch of signatures.
The user could create the signatures, the blind signatures for their credentials later.
However, we actually came up with a solution based on homomorphic cryptographic commitments, range proofs, and a blind signature scheme that works with this homomorphic cryptographic commitments in a way that we can actually come with an anonymity network identity, register input, get back something, come with another anonymity network identity, register another input, get back something, and we could combine the two something in zero knowledge that in a way that we could prove the server that we could make any kind of outputs out of those and we could have done it with these anonymous credentials in some way or form, but we would still have to have denominations in order to achieve some kind of privacy.
That was the thought of line there, right?

Speaker 0: 00:13:34

Just so I understand, instead of registering all inputs at once, you would be able to register them with different identities, right?

Speaker 1: 00:13:47

Yes, we can come with different identities with any number of inputs and we can come with different identities to register any output.
That's what we kind of figured out.

Speaker 0: 00:14:06

So you would provide a, let's say one Bitcoin input and another one Bitcoin input later and then you would get two one input one Bitcoin tokens and that could be used to add a two Bitcoin output or something like that and you don't have to show that your inputs were one Bitcoin you just show that the sum is equal to two bitcoins.
Yes,

Speaker 1: 00:14:35

in fact even more we can merge them and break them down in any way or shape or form.

## Explanation of breaking inputs, merging commitments.

Speaker 1: 00:14:44

I'm not sure, okay, I will risk because this this session is about anonymous credentials and I will bring up some topics, but yeah, I will risk it to explain it to you, because it's really interesting, and I think it's really know-well.
You can think about it, the breaking part is easy and I think that you understand it easily and I can explain it to you.
Because if you have one Bitcoin and you want to pay 0.1 Bitcoin to someone, then it would be like this.
You create two Pedersen commitments to 0.1 Bitcoin and to 0.9 Bitcoin.
Those will be your outputs in the coin join, right?
So far it's clear?
Yep.
So far it's clear?
Yep.
So, and then you register that two Pedersen commitment and Pedersen commitment for your 1Bitcoin input and you of course tell the coordinator that hey this 1Bitcoin input I'm going to prove that it is mine and this is the sum of my patterns and commitments.
By the way, we create more patterns and commitments with zeros, but it doesn't matter for now.

Speaker 0: 00:16:31

Yeah, that makes sense.

Speaker 1: 00:16:32

Yeah, And then we also found a blind signature scheme that works with feathers and commitments.
So the coordinator can give us something from what we can create a signature on our values, which is cool because then we can just come at output registration that, hey, I'm registering this 0.1 Bitcoin output and I have a signature on it.
And with another anonymity network identity, hey I'm registering this 0.9 Bitcoin output and I have a signature on it.
So this is the breaking part.
And the merging part is different because we couldn't figure out with the, with Pedersen commitments, range proofs and, yeah, of course, there needs to be a range proof along with the patterns and commitments, but I think that's obvious.
Anyway, we couldn't figure it out with the blind signature scheme on patterns and commitment, but we actually had to use BLS signatures.
And with that, we could figure out how to merge together more than one commitment.
Yeah, so it's pretty cool.
Yeah.
Any question on that or we can get back to this paper.

Speaker 0: 00:18:10

Yeah, I don't quite understand why that wouldn't work if you if you let's say have a point one and a point nine.
Talk Bitcoin token, right?

Speaker 1: 00:18:22

Yes.

Speaker 0: 00:18:24

Don't you just have to show to the server that both tokens sum up or maybe even better, you create a new token with a one Bitcoin value, you don't show the server your, or the value of the new token and but you show the server that the sum of the old tokens is the value of the new token.
Wouldn't that work for merging?

Speaker 1: 00:18:52

Your first suggestion, yes, that works.
It just, there is some probably negligible privacy loss, right, Like you expose the server that you have a 0.1 Bitcoin and a 0.9 Bitcoin pedders and commitments on the server.

Speaker 0: 00:19:13

I don't think, at least with anonymous credential slide, I don't think you have to do that necessarily.
I think you can show that the sum is the value of your new token and you don't have to show anything more to the server, I think.

Speaker 1: 00:19:32

With your first suggestion, I was talking about that, right?

Speaker 0: 00:19:37

Okay.

Speaker 1: 00:19:40

That's not a huge privacy thing, so it can work.
But we figured out how to do it even without that.
So your second suggestion, could you repeat it maybe?
I'm not sure I understood.

Speaker 0: 00:19:57

I thought I was only making one suggestion.
So perhaps it was that.
I'm not sure what the second one would be.

## Reissuance of tokens.

Speaker 1: 00:20:05

So your first suggestion was to take two blind signature of 0.1 and 0.9 and register them together to the server, to the coordinator, is that correct?

Speaker 0: 00:20:24

Perhaps I wouldn't call this registering, I would just call this like, perhaps like just a reissuance, We've used that term before.
You have a token and you just want to get a new one with a new serial number and these tokens are unlinkable and the same would work if you show two tokens and a new token where the new token is the sum of the former tokens and you don't have to show the actual values to the server you just have to show that the sum matches to the new value

Speaker 1: 00:21:03

and so

Speaker 0: 00:21:04

then you wouldn't have that privacy loss of having to show the individual values of the old tokens.

Speaker 1: 00:21:11

Yes, so the thing is we get the signature, the blind signature on the data itself.
Which means if we want a reassurance phase there, then we would have to expose the values.

Speaker 0: 00:21:33

Okay.

Speaker 1: 00:21:34

So there might be some some scheme that works with the, well with BLS signature we actually figured it out how to how to do that because there the signatures actually has the message itself.
So it's really fresh.
I just learned about it today.
And something like that, that you can give the two blinded BLS signature to the coordinator and prove that their sum is this value.
And because of the blind BLS signatures are the unique tokens, this way we won't have problems.

## Are denominations required by anonymous credentials?

Speaker 1: 00:22:28

So with anonymous credentials, I think you would have to, you would have to, to create a bunch of bunch of denominations.
Right?

Speaker 0: 00:22:46

I don't think so.
I think this is exactly the magic of these anonymous credentials that you can do these sum proofs similar to what you just described with BLS signatures.

Speaker 1: 00:23:03

Uh-huh, okay.
I, uh-huh, okay.
That's, yeah, that's really similar with what we came up with, indeed.
But I'm not sure in this paper.
Maybe I just didn't go into it.

Speaker 0: 00:23:21

Yeah, no, I if I remember correctly, perhaps they're not showing this in this paper.
But this is something that is like a central concept in the Brant's PhD thesis and I believe you can do the same thing with anonymous credentials because both types of credentials look actually very similar.

Speaker 2: 00:23:45

Look actually

Speaker 0: 00:23:45

very similar.

Speaker 1: 00:23:52

All right.

## Anonymous credentials vs BLS signatures.

Speaker 1: 00:23:55

I'm not sure if it, would it make sense to start investigating this instead of doing it with BLS signatures?

Speaker 0: 00:24:08

Actually I think I don't know I would do whatever is easiest actually Because I guess for your application or in general, it doesn't make too big of a difference if you use BLS.
I mean, if you think that parents are secure and BLS signatures are secure and this whole bunch of crypto assumptions, then I think you can just use that if that's easier.
I don't think you have to restrict yourself to something that works in the discrete logarithm paradigm.

Speaker 1: 00:24:45

Is the RnBLS signatures work on the discrete logarithm paradigm?

Speaker 0: 00:24:51

No, they use pairings.
So it's different curves and different cryptic assumptions.

Speaker 1: 00:24:59

Okay, All right.
So yeah, I'm not sure it is easier for us because the implementation, I think still looking behind of the BLS signature implementations.
So On the other hand, it's such a simple scheme that they could even explain it to me who doesn't understand crypto that much.

Speaker 0: 00:25:30

Okay, the BLS thing, does it have an implementation?
And if so, how is it called?
So I can find it.

Speaker 1: 00:25:37

I think it does not have implementation in C Sharp.
It has for a couple of languages.
I think the main implementation is C++ and there is bindings for that.

Speaker 0: 00:25:54

Okay.
I think there's an implementation of Brian's credentials in C sharp, right?
That's U-Proof library.
Okay.

Speaker 1: 00:26:02

Yes, I was playing around with that.
In fact, I ported it to .NET Core and it's not that obvious how to use that but the code is very, very clean and very nice.
So I would have loved to go with U-Proof.

## Problem's with proof. / Brands' credentials.

Speaker 0: 00:26:21

What's the problem with U-Proof?

Speaker 1: 00:26:26

Well, that doesn't solve our problem as far as I understand.
You still need a bunch of stuff to do with that.
Also people are talking about that it's not very secure and things like that.

Speaker 0: 00:26:47

No one's found a vulnerability yet, Brant's credentials, so as far as I know.

Speaker 2: 00:26:59

I don't

Speaker 0: 00:26:59

know, it's a difficult question, but I think the sum proof that I mentioned earlier should work just as well with brands credentials you don't need multiple denominations.

Speaker 1: 00:27:15

Because brands credentials would be able to prove the sum.

Speaker 2: 00:27:21

Yeah.

Speaker 1: 00:27:25

And does it have also, how would the range proofs apply to that?

Speaker 0: 00:27:34

Yeah, you probably still have to do these range proofs to show that the values don't overflow but I I'm not sure if the U-Proof library does that already for you.
I haven't really looked into the library ever.

Speaker 1: 00:27:49

And what else there is?
How about the merging of the coins?
I think that could be a problem there that you cannot merge two attributes together in a way that it both prevents double spending and you don't expose the attribute, you know, the values, only the sum of them.
I'm not sure that's possible.

Speaker 0: 00:28:30

I think it is.
I think that's the point of Brands Credential.
If you do a reissuance, you don't have to show all the attributes.
You just assure the server, you prove to the server that your new token doesn't have any other value than the sum of your old tokens combined.
I think, and this is possible with brands credentials.

Speaker 1: 00:29:00

You don't need the reissuance there?

Speaker 0: 00:29:04

Yeah you would need the reissuance.

Speaker 1: 00:29:07

Okay so now finally there is an argument why our scheme is better because we don't need reissuance scheme there.
But for a non-credentialed slide.

Speaker 2: 00:29:22

So I actually.
In there.
Okay.
But for unknown

Speaker 0: 00:29:22

credentials like, but okay, so I actually.
That sounds like something that BLS or pairings could do, like merging different credentials together without communication with the server.
So at least to me that sounds plausible.

Speaker 1: 00:29:40

Yeah, actually, I'm just going to read a few things about here is that you prove about you prove from the article that to be for everyone knows what we are talking about.

## Unlinkable re-use of credentials.

Speaker 1: 00:29:58

From the efficiency point of view, therefore, the YouProve credential system based on Brand's work acquired and implemented by Microsoft, seems attractive.
Uprove does not allow unlinkable reuse of credentials.
In order to unlinkably use a credential again, a user must get it reissued, which actually suggests that, in fact, that this paper doesn't have linkable credentials, only unlinkable.
These lines don't suggest that, but that's what's in the paper.
Let me see One more thing there.
When such a proof is carried out, it cannot be linked to previous uses of the same credential or any other identifying information about the user.
Ah, yes, This is what I'm talking about here.
We actually want the opposite.
In order to avoid the worst spending, we want a use to be linked to previous uses of the same credential which brands provide and this scheme does not, I'm not sure how hard would it be to implement it, Would it be only a simplification or this would be a major headache to implement linkable credentials on top of ACL construct?

Speaker 0: 00:32:00

On top of what construct?

Speaker 1: 00:32:02

ACL, this paper is anonymous credentials light ACL.

Speaker 0: 00:32:09

Yeah, I think that's easy because one of the attributes would just be the serial number that the server stores.
I mean the server stores the serial numbers of course that have been used right so okay that wouldn't I guess yeah you would need the reassurance again right you know it's all your serial number and then you get a new token.

Speaker 1: 00:32:35

That would also ruin the sum stuff that we talked about.

Speaker 0: 00:32:41

No. Why?

Speaker 1: 00:32:43

If you put a serial number into the attribute, then you cannot prove the sum.
I mean, the serial number is there, you know.

Speaker 0: 00:33:00

So what you do is you show your old credentials, can be multiple, you show the serial numbers for each of those credentials, you prove that the serial numbers are actually the ones contained in your credentials, the server checks that these serial numbers have not been used, you show the new token that you created with a fresh serial number that you chose randomly and then you do the sum proof and that way you don't have to show anything to the server but the serial numbers.

Speaker 1: 00:33:39

That's smart.
Isn't it just like if we would create blind signatures to as many attributes we...
I don't know.

Speaker 0: 00:33:57

Yeah, the problem is with blind signatures, right, is blind signatures are unstructured.
You just have this message and then you can put different things into the message but then you cannot efficiently prove anything about these individual attributes in your message and this is why these credential schemes are superior to the normal blind signatures.

Speaker 1: 00:34:20

Yeah, yeah.
All right.
So there may be something here to...

Speaker 0: 00:34:35

Yeah, I'd also like to look into this BLS stuff.
Definitely, that seems interesting.

Speaker 1: 00:34:42

Sure, I'm going to link the repository in the comment here, but don't share it yet because we did not figure out the name and we have a stupid name for the repo for now.

Speaker 0: 00:35:07

Okay.
Okay, I see.

Speaker 1: 00:35:12

Do you guys have anything to ask, odd, talk about, regarding anything maybe.
Everyone is really silent.
Go ahead, Lucas.

Speaker 2: 00:35:38

No, I have no question because I'm not, I don't know these primitives yet.
So, I have to study a bit more.

Speaker 0: 00:35:55

Yeah I learned most of that from, so Adam Beck he once gave a presentation about Brian's credentials at Blockstream So I learned a lot from him, but that wasn't public, unfortunately.
I think I have the slides, but I don't think they're very helpful.
So perhaps the best starting point is still Brian's PhD thesis.
It's very long, but just have to check out some parts of it, I think.

## E-cash.

Speaker 0: 00:36:24

Because especially the things like this anonymous credential slide, there seems to be the difficult thing about or to grasp about it is not I mean this scheme exists but the question is how do you use it and how do you use it with serial numbers and to get e-cash tokens with multiple denominations right That's not in the anonymous credentials light paper.
That's something that Bruns talks a little bit more about.

Speaker 1: 00:36:56

And even more because As we reviewed this paper and we looked into that, well, how could we use it for e-cash kind of stuff, then we just stumbled upon a tremendous amount of literature there that how to do divisible e-cash systems and it's really like a couple of hundred of paper is going on this issue.
But the thing is they are solving things that we don't need to solve because coinjoins are inherently secure.
If someone doesn't see their outputs, then it's not going to sign.
And that's a huge help here.
So our job is basically to simplify what they have.

Speaker 0: 00:37:54

Right.
There's also the concept of offline e-cash, which also doesn't seem to be very practical in the Bitcoin world, because in offline e-cash, if you double spend, you reveal your secret key, which perhaps as if you're an attacker that's not a big problem to you because you already have your Bitcoin so you don't care about the secret keys in your token.
You have twice as many Bitcoins as you would have normally.
So they don't seem to apply.

Speaker 1: 00:38:25

Yeah, that's not even a requirement here because everyone is online.
In fact, even all the participants are online, although you're not.
Yeah.
Okay.
But this

## Next steps.

Speaker 0: 00:38:39

idea of merging inputs and so on, that's really interesting, I think.

Speaker 1: 00:38:45

Yeah, we are going to work on that and either look into that issue, that's where we figured out how things should be, but we are going to create a draft and send it to the Bitcoin dev mailing list and things like that.
And also for the next Wasabi Research Club, István is going to...
Actually, yeah, he is going to write down exactly this scheme, the cryptography part of it.
And that's what I would like to propose for the next Wassabi Research Club, because as we looked through e-cash papers and anonymous credential papers and every kind of papers, it looks like this is the simplest and most straightforward solution for really arbitrary coin joins, which we are not going to do but we would like to have that flexibility and that's what lets us improve upon it in the future.
Max asked what about server decided equal value outputs?
Anyone understands the question?

Speaker 0: 00:40:11

No.

Speaker 1: 00:40:15

All right, sorry, Max.
We can't reply you.
Okay.
Oh yeah, one more interesting thing.
Max figured out that Foteini, one of the authors of this paper we are talking about, actually had some involvement in Tumblr a bit.
Not sure exactly what, but yes, she was doing something in Tumblr a bit.

Speaker 2: 00:40:45

Something in

Speaker 1: 00:40:46

time a bit.
And I think if no one would like to say anything because this was quite a difficult paper, was quite a difficult paper, then we can cut this short unlike other conversations and we can go.
So Do you guys have anything else you would like to talk about?

Speaker 2: 00:41:21

Not yet really.
I mean, I'm just fascinated about the things that you guys talk about.

Speaker 0: 00:41:30

Yeah, I think I talked about almost everything I know about it, so let me know how this progresses and what you find out.

Speaker 1: 00:41:42

Yeah, definitely.
We are going to talk about our scheme and the next Wasabi Research Club, if no one has an objection.
Or alternatively, we could review Adam Gibson's from zero knowledge to bulletproofs paper.
I think that could be useful or our scheme, which might make more sense, to be honest.
But it could change.
Maybe we figure out how there is something utterly wrong with this and the next week would be pointless.
But I doubt at this point.
We really reviewed a lot of things last week.
So Should the next generation wasabi mixing technology be the topic of the next wasabi research club?
What do you guys think?

## Equal value denominations.

Speaker 3: 00:42:59

Yeah, I think It's good.
But there was a question from Max, that is there a difference of users who want to be a part of the equal value denomination and those who want only specific amounts?

Speaker 1: 00:43:14

Yeah, no, There is no difference.
It's equal value denominations as I imagine it right now, although we did not work this out at all.
But I think that could be something that the users create by themselves.
So if I participate in a mix, then I'm going to ask for outputs of some standard denominations that I guess I estimate other users, I suspect other users are going to do too.
So that would be it, but I could create outputs in any way, shape, or form, up to the maximum limits, of course, As I would like to even do a pay to end point transaction in a coin join which would be neat.

Speaker 3: 00:44:15

Yeah, that sounds good.
Damn, that sounds good.

Speaker 1: 00:44:19

Also a really interesting thing, we just had a talk with Todj, one of the guys who came up with the Lightning Network and he actually came up with a coin swap protocol.
There is still some denial of service issues he didn't figure out, but he came up with a coin swap protocol that after top route is in Schnorr and top route is in Bitcoin, their top rooties in Snorrent, top rooties in Bitcoin, then he could do coin swaps, those could be completely unnoticeable and That's really exciting.
So I just wanted to share this This fresh information Okay All right.

## End.

Speaker 1: 00:45:24

Thank you, guys.
And I'm sorry for this unconventional Wasabi Research Club now.
Usually Aviv does a very good job at explaining the concept at the beginning, but he couldn't make it last minute.
So no one could really prepare, but Nick gave a great summary of the paper.

Speaker 3: 00:45:54

Absolutely.
I mean, you guys did a good job.
And thanks for that.

Speaker 1: 00:46:00

Yes, thank you, Nick and thank you for being the special guest of this episode.

Speaker 0: 00:46:08

What an honor.

Speaker 1: 00:46:12

All right, then I guess that's it.
Like, share and subscribe bye bye

Speaker 0: 00:46:23

bye everyone

Speaker 2: 00:46:24

bye guys

Speaker 3: 00:46:25

bye

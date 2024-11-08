---
title: How to Design Schnorr Signatures
transcript_by: Shourya742 via review.btctranscripts.com
media: https://www.youtube.com/watch?v=wjACBRJDfxc
tags:
  - schnorr-signatures
speakers:
  - Adam Gibson
date: 2022-03-14
---
## Passwords

So, I'm going to talk to you today about passwords and about the problem with passwords and how we might be able to solve it, right?
So we're all familiar with using passwords on the internet and we're all sort of sometimes annoyed about it.
Maybe you use a password manager, maybe you don't, but you have this problem, I think we all understand this problem that it's not just about you losing the password, but it's also about keeping it secret, right?
So when you enter a password on a password form, the problem with that is, if you're technical, you'll understand that there's a problem with it that you're sending a secret across to the server.
Now, okay, you may be sending it over an encrypted connection, So that's obviously better than just sending it in plain text because no other person out there can steal it.
And you might trust the server to behave responsibly and put the secret in a hash form into a database and not reveal it to third parties and so on.
But fundamentally, it's kind of a crappy model.

## Public key Cryptography

So a long time ago, people came up with ideas, at least, on how you could do this kind of thing better.
And a lot of those ideas, although many of them haven't really been realized, some of them have, were about public key cryptography and it's the same kind of cryptography we use in Bitcoin.
Specifically the idea that you have a public key, we can call it `P`, and you have a private key we're going to call `x`.
So in the rest of this explanation, I'm going to be focusing on the idea of a number `x` being a secret.
Of course, you know, your password might be a phrase, but a phrase of letters can always be transferred into numbers.
So just think about things in terms of numbers.

So we have a number `x`, maybe it's a very long number, and we have public key cryptography, which kind of converts that number into a public key.
And in Bitcoin specifically and some other systems, what does that really mean?
It means taking that number `x` and multiplying it by a point on the elliptic curve which in Bitcoin is called secp256k1.
But even then I have to be a bit more careful to explain what I really mean.
What does it mean, multiply a number by a point?
Well as to what a point actually is you're just gonna have to accept the idea that you know elliptic curve consists of a bunch of points and they're in what's called in mathematics a group.
And the group has a certain order, which means the size, it's just a technical term for the size of the group.
So think of it as a list, this huge list of points, there's about `2^256` of them, so it's a huge list.
And what we really mean when we say `x*G` is something like this.
We take some starting point `G` that everyone's agreed on.
So secp256k1, which is the bitcoin curve, has such a specific point `G` which you can write out as a big string.
And what you do is you take that point and you add it to itself.
And because it's a group with an additive operation, it means we can actually do that.
We can take the two points and add them together.
I won't get into how you add them, but there's a specific operation.
It's not literally adding numbers, it's something else, but it has the same effect.
Now if I add the point to itself, of course, intuitively I hope it's kind of obvious what that should be referred to as `2*G`.
So `2*G`, meaning `G+G`, so it's going back to literally what you learn when you're six years old or five years old at school, how to add numbers together, or how to multiply numbers is to add them a certain number of times.
So `x*G` literally does mean `G` added to itself `x` number of times, where `x` is this unfathomably huge number that we call a private key, right?
So we all know about that idea of a private key being a huge number so nobody can guess it.
And we're taking that huge number and we're adding `G` to itself that huge number of times.

And you might reasonably wonder, is that even remotely possible?
Doesn't that take forever?
Oh, there's some tricks.
I won't get into it now, but there's some tricks to make it possible to do that.
I'm really sort of focusing on that now because everything we're gonna do after this depends on that.
All right, so getting back to the point, the point about passwords.
We wanna use like public key cryptography to make it so that we don't actually send that secret, which again could be a phrase or could just be a number.
We don't want to send it to the server and have to trust the server not to screw up, lose it, give it to someone else, or whatever.
We don't want to trust them.
We just want them to only have that public key.
And somehow we want them to accept that we know that private key that corresponds to the public key without ever giving it to them.
It's one of the great achievements, arguably, of public key cryptography, is to find a really good algorithm that makes this happen.
And now, in order to explain how it works, we're just going to take a few steps.

## Commitments

What we're going to explain first is the idea of a commitment.
I think the best way to explain a commitment is to use a really real world, if admittedly a bit silly example, which is flipping a coin.
We're all familiar with the idea.
Suppose I've got Alex here and he and I we want to go out to dinner tonight and we're either gonna have Well, I want to have steak, but he wants to have fish.
Let's say he doesn't like steak.
Whatever.
I'm gonna flip a coin It's gonna enable us to decide right?
I'm gonna flip a coin bang, right?
So what have I just done?
I've flipped the coin and I've held it in- I want you to focus on something maybe you don't usually focus on when we do this, but what exactly is going on here?
Probably in your head you already have the idea that by doing this I'm sort of fixing the value of the coin, right?
So we could call that a binding effect, like literally sticking it into one thing.
Also, very critically, equally important, is that I can't see it, right?
Notice that I can't see the result of the coin before we decide on the final step.
So, call the coin Alex.
Okay, so Alex says it's tails and he has some confidence that when it gets revealed it will be fair.
So why is he confident it'll be fair?
I would say he's confident because he knows I can't do this (flip the result) without him noticing.
He already noticed what I just did, right?
I also can't do this (look at the result) without him noticing, right?
So what does that mean?
It means that, as I just said, it's binding.
I can't flip it under my hand, but it's also hiding.
I can't see it.
So these hiding and binding properties are critical.
So you called heads, and indeed it is heads, so well done - you won this coin.

My point in illustrating that is it's really important that we have those two properties, hinding and binding.
And I think really nicely illustrates why that's important and why it's more difficult on the internet is if we consider, well what happens if me and Alex did the same thing, but instead of being in the same room together and he watches me, let's say we're talking on a telephone line.
So in that case, let's say we have the same problem, we've got to decide where to go for dinner, and I'm on the phone saying, "hi Alex, we're going to decide where to go to dinner now, I'm going to flip the coin now".
Well, that wouldn't be very good at all, would it?
Why not?
Why not, Alex?
[Alex's response]: "Well, because you could lie to me." Exactly right.
So I could lie.
So I could say to him, because remember it's kind of a two or three step protocol, he's got to tell me what he decides, right?
After I've supposedly I flipped the coin, but he hasn't seen me, he's gonna decide and say, "oh I call heads", and I'm gonna say, "well no, it was tails".
And how's he gonna know any different?
He doesn't know if I flipped the coin and looked at the result or if I just didn't flip the coin at all.
Of course, more likely, I just made it up.
So this kind of protocol completely fails if you're not there to ensure that hiding and biding property.

But the interesting thing is, it might be possible, in fact I think it is possible, for us to follow such a protocol using some basic cryptography.
What basic cryptography?
So if you're out there listening, you might think how would you solve that problem being on a telephone line but trying to follow that same protocol.
And so you might think of this idea, which is a good idea, use what's called a hash function.
So something that anybody who's been in Bitcoin knows about, is this idea of a hash function where you take some data and you put it into a hash function as input and you get output a certain value: `H("heads") -> y` .
I don't know why it's called `y`, it just is.
All right, so let's say in that case, what Alex would be doing is taking his decision, his call, his choice, heads, putting it into a hash function like sha256 or any other hash function that's cryptographically secure, and getting out an output value.
He would tell me the output value.
I would say, okay, you've made your choice.
You can't go back on it.
It's binding, it's a binding decision.
I'm going to reveal the result of my coin flip.
I could just choose a number of 0 or 1 on a computer or I could just make it up in my head, doesn't really matter.
And then when I choose it, I can then ask Alex to reveal what was actually the input that was given to our hash function.
And because the theory goes that a hash function is a one-way function, that's why we're using a hash function specifically, a one-way function.
The theory goes that when he tells me why on the phone, I can't figure out that it was heads that went into the hash function because given the output of a hash function, you can't figure out what the input was.
That's the general idea of a hash function.
But this protocol is kind of crappy.
Don't you think, Alex, maybe this protocol, what might be the problem with it?
It should be clear to anyone that the reason this isn't any good is because I'm sitting here being the guy who's flipping the coin, waiting for him to call and give me this hash output, but I can just check his hash output against two possibilities, the `H(heads)` or the `H(tails)`.
Because I can easily compute those myself in advance and I can just check which one of those two values it is and then I know what his call was and I can cheat and tell him it's tails.
So that's terrible but the nice thing about hash functions is they have special properties.
And what he can do instead is this.
He can make his choice heads, but then he can append, and I'm just using those two lines to mean add more data, some more data, one, zero, three, four, six, five, two, whatever, in other words some very long random string, could be a string, could be a number, doesn't matter.
He can get his output `y` from that instead.
Now I can't have a little lookup table of all the possible random values with heads and all the possible random values with tails because it'd be huge if this number is very big.
So the solution here is to have him commit, but commit in a special way.
He's committing and it is binding but it's also hiding.
This has a hiding property.
So this commitment is both binding and hiding.
Now it might not be obvious why it's binding, because you might think to yourself, I make this hash output `y`, but I've got all this area of free variables, I can just randomize this as many times as I want.
So I might be able to find hash tails and then a different set of random numbers, three, nine, eight, six, two, da, da, da, giving the same output `y`.
If I could do that, then I could cheat, yeah?
I could commit to one value, but actually then reveal the other value instead.
That's exactly why we need hash functions to have this property we call second pre-image resistance.
Pre-image being the thing inside the brackets there, the parentheses, and pre-image resistance or second pre-image resistance meaning that once I've found one output I can't then find a second input that gives the same output.
So that's why certain kinds of hash functions which aren't cryptographically secure are not suitable for cryptographic protocols because they don't have this special property of first and second pre-image resistance and collision resistance.
If you want to get into it you can look it up.
Okay, so that's how we would solve this problem of wanting to have a fair game where we make a fair decision.
But this is not quite the same problem that we were originally trying to solve.
What we were originally trying to solve was to prove that we know a secret but without revealing it.
The problem with this protocol in solving that is that Alex has to reveal at the end.
He has to say to me, yeah, actually my input was `heads|1034652`.
He has to actually tell me that at the end, otherwise I don't know whether he performed the protocol honestly.
Okay, so we haven't solved the problem, but we've kind of got a sort of movement in towards solving it by finding this commitment system.
And we've learned something very important that a commitment has to be both hiding and binding.

## Commitment Scheme + Challenge Response

All right, so let's move on then taking this knowledge and see if it can help us to solve the problem of how do I prove I know the value `x` that gives the public key `P`, which is equal to `x*G`, which we just discussed, without on the other hand revealing `x`.
And the solution is a blend of what we just said, a commitment scheme, which we're going to use very extensively in various ways, but also the idea of challenge-response.
So I want to give you a kind of intuition as to why a kind of challenge response element is going to be important here.
I suppose I was like a world-class chef and I had this special signature dish that everyone in the world thought was just the most amazing dish, and everyone was paying thousands of dollars to eat at my restaurant, because this special dish was so special.
And you might say to yourself, you might meet me and not be sure that I'm actually that chef, and you say, well, I need to prove that you're actually that guy.
And I'm saying to you well I'm not going to tell you my secret ingredients or my secret special sauce that makes this amazing dish because then you'll just take it and you'll be making all the money.
So we were in a bit of a standoff and it's kind of similar to this one but it's different as well because I don't want to reveal the secret.
So one you could imagine it just completely taking cryptography out of the equation like how would you solve that problem?

Well one way of approaching it is a kind of a proof, an operational proof.
Proof by doing.
So what that would mean is you would take me and you would put me in a kitchen, and not just any kitchen, but you would completely isolate the kitchen.
There's no windows, there's no internet, it's literally a Faraday cage, nothing can get in or out.
And there's every possible ingredient under the sun.
All the ingredients are in there.
And that's to make sure that I can make my dish.
Because you don't know what ingredients I need, but I might need certain ingredients.
So you're going to just stuff it through every ingredient imaginable in this kitchen.
And you're going to lock me in there for an hour or two hours, whatever it takes.
And if I come out and give you the dish and you can taste it and say, yep, that's definitely the real McCoy, that's the real one, then you'll say, yep, I believe you.
You're the guy who knows the secret.
But I didn't learn the secret.
And specifically, of course, that's because I had to give you all the ingredients.
If I only gave you a specific 10 ingredients, I could probably just figure out the dish from the ingredients.
So what's the intuition there?
The intuition there is that somehow by giving this person a fresh challenge, a fresh instance of a challenge to solve, if they can solve it, then they must be the guy that owns the thing.
So that's why challenge response comes in with commitment.

## Failure in hiding

All right, so let's think in particular about that idea of challenge to start with.
We're now gonna move from something weird and like a chef down to literally just numbers.
Remember a private key is just numbers, or a number.
So let's configure it and say there's waxwing me who's claiming to know this `x`, and there's Alex who's wanting to challenge me and verify it.
So I'm gonna be using like `W` for me, waxwing and `A` for Alex.
`P` is known in advance, `P` is the public key.
We both know it, I'm claiming it's mine, he knows what I'm claiming.
He sends me a challenge, and from now on, that challenge value is gonna be called `e`.
And this, just like a private key, is just an integer.
I'm gonna take that challenge, and I'm gonna multiply it by my private key.
So the point here is to try and sort of embed the private key into the challenge.
I'll call that value `s`.
So I'm going to send `s` to him.
Now, The idea is that I couldn't have sent `s` if I didn't know `x`, but I don't want him to know `x`.
So the theory is, that when he takes the `s` and he multiplies it by `G`, just like you would with a private key, what's he actually gonna get if he does that multiplication?
Well, we know that `s = e*x`.
He doesn't know `x`, let's say, but he knows, or we expect that it's `e*x`.
So that's `(e*x)*G`.
But if you look at that you can see that actually that's `(e*x)*G = e*(x*G)`, and `x*G` is the public key.
So that's actually `e*(x*G) = e*P`.
So what he can do is he can look at that `s`, multiply it by `G`, and compare it.
He can compare it with `e`, which he knows because he generated it, that's the challenge, and multiply that by the public key `P`.
If these two things are equal, the claim is that I did actually know the value `x`.
Just in the same way as `P` corresponds there.
All right, so first of all, do you agree Alex that that proves that I know `x` if I send you that `s`?
[Alex's response]: "Yeah, because that's the only one that could satisfy that, right?" Right, yeah, because if I didn't have `x`, if I put in something else instead of `x`, this wouldn't balance.
But nevertheless, this idea is completely broken.
It doesn't work at all.
Why doesn't it work?

So if we look at this quantity here (`e`), remember what we said, it's an integer.
Now, dividing integers is a little bit more complicated here than in school, dividing 72 by 31 or whatever, it's a little bit more complicated because we're in what's called modular arithmetic, which means we're dealing with integers up to a certain maximum value, and then it's sometimes called clock arithmetic, you go around.
Although it is more complicated, it's only a little bit more complicated and is actually pretty easy to find.
In modular arithmetic we might say the modular inverse of `e`: `e^-1`.
Modulo `n` where `n` is the order of the group.
The point is that it's actually very easy for him, to take this number `s`, take the number `e`, and take its modular inverse, and you can see just by the division on this side, that's gonna give you `x`: `s = e*x => s*e^-1 = s*e^-1*x => s*e^-1 = x`.
So the problem with this approach was that although it had that binding effect, it didn't have the hiding effect.
It was very easy to extract the secret `x` from the "signature" or response value `s`.
Okay, so this approach fails.
But the challenge response idea is there.

## Failure in binding

All right, so because we failed to hide the private key in this case, let's try and take a different approach.
Let's try and actually hide the private key.
It's pretty important.
So we'll have the same setup, Waxwing and Alex.
What we decide to do here is take the intuition that if I add a number to `x`, then it hides it.
So for example, before I sort of write out the equations, if I gave you, Alex, the number 13, and I said which two numbers were added together to make that, what would be your answer?
[Alex's response]: "There could be 1 plus 12, and all the other combinations"
Exactly.
So it doesn't tell you.
Now if we extend that from 13 to a number that is 256 bits long then it's a huge number of different combinations of numbers that could give the result.
I mean, technically any of the numbers could be the result and that's an important sort of theoretical point.
But anyway, the point is, if you just add two huge numbers together then it's going to blind what the first one is.
The first one is going to be hidden by that process, that's the key idea.
All right, so that gives us the intuition that all we need to do is take another number which we're going to call `k` and add it to `x`.
So this new protocol is going to say, right, I'm going to choose a new secret number `k`, and I'm going to calculate capital `K`, just as the previous examples, you're taking a private key and multiplying it by the generator point `k*G = K`, and you're getting the capital, so to speak, public point or public key of the corresponding secret there.
Now, you might be wondering, what am I doing?
Well, what I'm doing here is actually committing.
I'm gonna send that capital `K` across to Alex, all right?
In this particular example, I'm going to send you `K` first and then I'm just going to take `k+x`, the secret values, add them together and actually send you that as `s`.
So, without knowing `x`, how are you going to verify that `s` proves I knew `x`?
Well you're going to take `s*G` again, and according to the formula, again you don't know if it's true yet, but if it's true that will be `(k+x)*G`, and that will be equal to `k*G+x*G`.
And we already know that that must be equal to capital `K`, and `x*G` as we've been seeing in previous examples is the public key of `P`: `k*G+x*G = K + P`.
So again, you could do a verification where you check whether `s*G` does actually equal to the original `K` you were given plus the original public key `P` you were given.
And if it's true, then the theory is, therefore I knew the private key.
But, what do you think Alex?
Is there a problem with that?
[Alex's response]: "Well, yeah I think there is a problem with this one also".
Yeah, unfortunately this was a little bit more difficult to understand.

I'll sort of give the spoiler alert and say that this is often called a key subtraction attack, or maybe a related key attack.
It crops up in different forms, but this is the most basic form.
Unfortunately, It looks a little bit confusing, but the core insight is that I'm making these choices without you intervening.
So basically what I'm saying is, I can choose this (`K`) to be whatever I want, and specifically, I can choose this to be of such a form that the final `s` value does not depend on the private key at all.
And if I can choose this `s` value in such a way that it does not depend on `x` at all, then I don't even need to know `x` in order to satisfy the protocol, which means that this would fail to bind.
So let me show you how that works.
If I make the `K` value, equal to a different `K` value, `K = K'-P`, which I definitely know, we always both know the public key `P`.
But in this case I'm cheating, I don't really know the private key.
So what I do is I take a different one,I started with `k'*G = K'`.
I took that and I subtracted the public key.
You tell me, what is the private key of capital `K`?
[Alex's response]: "It's gonna be `G` times whatever it had there".
No, so this, so if we do it in steps.
What's the private key of `P`?
[Alex's reponse]: "That's going to be `k*G`".
No, that's `x`, isn't it?
That's the public key of the key that we're trying to prove knowledge of.
So the private key of `P` is `x`.
And I've chosen the private key of `K'` is `k'` there.
So what the private key of `K` will be, will be `k'- x`, right?
`K = K' - P => K = k'*G - x*G => k*G = (k' - x)*G`
So when I calculate `s`, `s` will be `k + x`.
Now `k` is the private key of capital `K`, so that private key is in fact `k'-x+x`.
`s = k + x => s = (k' - x) + x => s = k'`
By doing this I've created a cancellation of the private key in the formula.
By creating that cancellation, all I'm gonna do here is, as an attacker, as a person who doesn't know the private key but is pretending to, I'm gonna be sending `k'` as `s`, because that's all it is in this case, and it will satisfy the protocol.
Now, if that wasn't clear and obvious to people, I absolutely don't blame you.
It is really, really not that obvious.
But if you go through it, it should make sense.
The core concept is that you can subtract out the private key if you're not sort of forced to bind to it.
So this is a failure of binding in our commitment.
There's no binding.
Technically it's called, this is not a sound protocol.
And remember, this was a failure of hiding (referring to previous example) because we revealed the private key.
So in both of these cases we failed.

## Schnorr Identity Protocol hiding & biding

So clearly the correct idea is to combine these two failures together and make a new protocol which combines them both.
So what's the idea there?
We have the same setup as before.
We still have the public key `P`, we still have Waxwing on one side as the person trying to prove, and we still have Alex on the other side as the person trying to verify and check if the proof is right, just like the guy who was going to taste the chef's food.
Alex is going to taste the chef's food.
But what Waxwing does this time is recognizes the failure of the two previous cases and corrects each of those failures by combining the two ideas together.
So, as before, we're going to commit to `k`.
By the way I might not have explained, but we talked at the beginning about hash functions being used as commitments.
We can also use elliptic curve points as commitments.
It's kind of a slippery concept.
We calculate this capital `K`, `k*G = K` and we send it to Alex.
Alex receives it, but this time, just like in the first case, but not in the second case, where we forgot to do it, Alex is gonna send a challenge value `e`.
Remember, it's just an integer.
And now Waxwing is going to both hide and bind.
So he's going to hide by adding his `k` and he's going to bind using his `e` that's given to him by Alex.
That forces him to bind to `x`.
`s = k + e*x`
So we would send this value `s` to Alex and by now you should probably be able to figure out what Alex is going to do with that `s`.
What are you going to do with that `s`, Alex?
[Alex's response]: "I'm going to multiply it by `G`".
Great.
`s*G`.
But here's the tricky part, well it's not very tricky, but what is it equal to?
Well, as before, we're going to assume that the guy was being honest and see what happens.
So we're going to put `k+e*x`, which we don't know as Alex, but we're seeing what happens, and multiply that by `G` and we distribute that out.
`sG = (k + e*x) * G = k*G + e(x*G)`
I'm putting brackets there because `x*G` of course is exactly what `P` is.
And `k*G` is exactly what `K` is.
So `k*G + e(x*G) = K + e*P`.
As before, Alex is going to verify whether or not `s*G` does or does not equal to `K`, which was sent to him at the beginning, plus `e`, which was his challenge, times the public key `P`.
And if it is, he's gonna accept this protocol.
And this one we can prove does actually do the job that we want to do, which is that it gives Alex this certainty, the binding property, that I couldn't have done this without owning `x`.
And there's a very ingenious proof of that, which I will let you figure out, research later yourself.
There's a very ingenious proof of why it's not possible for me to have constructed this `s` without knowing `x`.
But equally beautiful proof is that it's not possible for Alex, remember the taster of the chef's food, it's not possible for him to actually learn any information about what `x` was from this protocol.
It's called the zero-knowledgness property.
What I presented to you?
You might think, oh, he's explained to me the Schnorr signature, right?
But actually I didn't.
I didn't actually explain the Schnorr signature.
What I explained is something called SIDP.
Sometimes it's written like this.
So Schnorr Identity Protocol (SIDP), not Schnorr Signature Protocol.
And what's the difference?
The difference is specifically in this thing here (points to `e`).
This thing here `e`, which we've been calling it the challenge.
We said earlier on, we need a commitment scheme, but we also need a challenge response scheme.
By the way, if people want to look this stuff up, it's called a Sigma protocol generally, but that's not interesting here.
So basically, this challenge, remember, was something that Alex generated, and it really would be a random number.
Obviously you could choose it if you wanted to but generally it just needs to be random and unpredictable to me.
The key thing is I shouldn't be able to predict it.
So this is a really good way to prove that you, let's say, you can have a login system.
An example is LNURL-auth in the Bitcoin world, which is used by sites like lnmarkets.com or stacker.news and a few others.
And the idea there is specifically what we mentioned right at the start, which is that we really want to be able to just have a public key and then do some weird interaction and prove that we own the private key without ever actually sending it.
Of course you don't want to send somebody the private key of your Lightning node, that's crazy.
So this kind of SIDP protocol like this satisfies exactly that requirement.
There are other schemes which I haven't really researched much, like [SQRL](https://www.grc.com/sqrl/sqrl.htm) by Steve Gibson has a similar scheme using, again, QR codes.
It's very often QR codes, and then you have this kind of challenge interaction.
But the funny thing is that a lot of those schemes don't actually use this exactly.

## Non-interactive Schnorr signatures

They use the Schnorr signature.
And so to come back to my point, what's different here with the signature compared to this identity protocol?
Well, the difference is in `e`, because what you can do is embed, inside this whole process, another commitment.
It's weird how this is like commitments inside of commitments inside of commitments.
So this `e`, we don't want it to be predictable by Waxwing, but that doesn't technically mean that Alex has to generate it and give it to him.
We can make it non-interactive.
We can make `e` be the hash of earlier things.
So specifically, this value `K`.
If we include `K` in this hash, and of course if you're making a signature, you wanna sign a message, so you might put a message in there.
And for reasons that are technical or perhaps obvious, we also want to include the public key `P`.
If we make `e` literally be equal to that (`e = H(K,m,P)`), then the beautiful thing is we've made a non-interactive protocol.
Now why is it non-interactive?
Because it's literally a case here that Waxwing would first generate his `K`, then he'd calculate this hash, because he knows `P`, he knows his `K`, and he knows his message that he's trying to sign.
So he can formulate this hash (`H(K,m,P)`).
But the beautiful thing is, having formulated this hash, he can't then go back and change `K`.
Because if you remember, this was a difficult one to understand, but the problem with this approach (showing the previous approach that failed to bind `K`) was that I could kind of go back and fiddle around with `K` and I could change `K` to be something that I wanted it to be.
No, that doesn't work here.
Once you choose `K` it gets fixed into this challenge value (`e`).
By the way, if people want to look up what the hell I'm talking about.
This is called the Fiat-Shamir transform.
Not the Fiat currency.
The Fiat-Shamir transform is this mechanism whereby we take the start of the protocol and we sort of hash it.
And by hashing it we kind of freeze it, because remember we can't find second pre-images of hashes, right?
So once we've found this `e` by doing that, we can't then go back and find another `K` that gives like `K'`, and maybe some other message that gives the same `e`.
We can't do that.
So it's all fixed up front.
So non-interactively, I calculate that hash, and I put that hash inside this `s` value and that creates the Schnorr signature protocol, which is non-interactive.
The Schnorr signature protocol is basically SIDP, but with a challenge being this hash value.

## Usage IRL

Last point I suppose is to address this question of, do people use SIDP in the real world?
Or do they use the Schnorr signature protocol, indeed, in the real world?
Now, on the second point, it depends on how you define Schnorr signature, but if you include, for example, Dan Bernstein's curve implementation of basically the same thing, then it's used literally everywhere, all over the internet, on TLS.
You've got it in other crypto protocols like SSH, and you've got all kinds of things.
And if they want to prove identity, you have this interesting point that a signature protocol is better than SIDP because it's non-interactive, which means that I don't have to have Alex there when I prove that I own a private key.
I can create a signature, give it to someone else, someone else can give it to Alex later.
He doesn't have to be around, he can be asleep, whatever.
So that's great, non-interactive.
But the weird thing is, as well as it being a really good thing, it has a bad side.
Because consider this.
Suppose I want to prove I'm super rich.
I've got 10 Bitcoin, 100 Bitcoin, whatever, and I'm just going to say, look, there's this UTXO on the blockchain, it has 100 Bitcoin in it here.
I'm going to sign a message from that UTXO.
I'm going to say, Adam is the owner of this 100 Bitcoin, right?
So I make a signature and I give it to you.
Now I want to ask you Alex, if I gave you such a signature in real life, and for whatever reason I wanted to, people don't usually want to do this, I wanted to prove to you that I have 100 Bitcoin and I gave you a signature and you could check on the blockchain, the UTXO, would you believe that I have 100 Bitcoin from that?
[Alex-response]: "Well not necessarily, you could have asked someone to do that for you, right?" Right.
And it's something that people don't often consider, or they consider it and they think, well, that's not very likely.
It's true it's not very likely, but you know, maybe there's an incentive.
Maybe Bob owns 100 Bitcoin on a UTXO, and I just have to give him like a thousand dollars or some large amount of money, I guess, because he's rich.
And I might just convince him to actually sign it and say, put my name on it.
And so you say, well, that doesn't really fully prove it.
It kind of does and it doesn't.
And that's exactly the negative side of non-interactivity.
Exactly because that signature is transferable means that you don't have the same kind of 100% proof.
What's really funny is that what people end up doing is they end up embedding the challenge response element of the original SIDP on top of the Schnorr signature to reintroduce the interactivity.
So they'll do things like, okay, you're gonna sign a message from that UTXO, but I'm gonna tell you a particular message you have to sign.
So they add in an extra interactivity.
So it's like layers upon layers of commitments and layers upon layers of interactivity and like commitment on top of commitment.
It gets really confusing.
But of course in reality the real world is that because signature protocols are so useful in so many contexts, they're in every cryptographic library out there.
Every single one of them has digital signatures.
Very few of them actually implement ID protocols as such.
I don't know if that's a fair statement.
I think it is.
And so very often people will build protocols, an example being LNURL-auth, which uses a signature, not an identity protocol, in order to prove identity.
So I hope I haven't completely confused everyone in that extremely long spiel, but there you go.

## History of Schnorr Signatures

[Alex's question]: "I have a question, which one of this was invented first, actually?"
Yeah, well, Schnoor's original paper, and I'm going to be wrong on this because I'll be vague, was sometime in the 80s, maybe the mid-80s.
He wrote a protocol, something about efficient protocol for smart cards.
Specifically, he was trying to come up with something very short and compact, because in those early days of public key cryptography, all the initial strides forward were made in the area of RSA, which is all about, instead of using elliptic curves, it was using modular arithmetic.
So you would have a public key which was literally just a number modulo some very large, well actually literally the public key would be the modulus plus the exponent and then the private key.
But anyway it was all just numbers and integers and these numbers were very large and so a lot of the clever protocols they came up with including things like this, I can't remember exactly weren't very compact.
So Schnorr's original goal, I think I'm correct in saying this, when in creating this protocol that I've described here was to prove identity for things like smart cards.
And then later, I think, I might be butchering this, but I think he came up with the signature protocol itself somewhat later, around about 1990 kind of time.
And he patented it, and then there was a whole saga about that.
And the reason we have ECDSA at all is, as far as most people understand, it's kind of folklore now.
It's mostly because Schnorr patented this design, which is the most elegant and simple design.
And my whole purpose in showing all of this was to show that It almost just comes out naturally.
It's not like some weird concoction.
It's just like an almost logical inevitability.
And ECDSA was a kind of a butchered version of the same thing that got standardized in around the early 90s because they couldn't use Schnorr because he patented it.
So that's kind of some of the history.
[Alex's response]: "Yeah. Oh, this was really great, actually.
So shill us JoinMarket.
Shill us something.
You have to shill something, anything".
I'll shill you Schnorr signatures.
They are very elegant.
And we haven't even got into why they're better than ECDSA.
It's because they have this linearity property.
That's kind of complicated.
[Alex's response]: "Maybe in the next video.
Anyway, This was it."
Thank you.

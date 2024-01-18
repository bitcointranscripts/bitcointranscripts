---
title: "Foundational Math, ECDSA and Transactions"
transcript_by: kouloumos via tstbtc v1.0.0 --needs-review
media: https://www.youtube.com/watch?v=e6voIwB-An4
tags: ['cryptography']
speakers: ['Jimmy Song']
categories: []
date: 2017-11-02
---
All right, so I was sitting there and looking at my own slide and I realized that there was a couple of very embarrassing mistakes.
First, the repo that you're supposed to clone is actually Bitcoin Edge Dev++, not Jimmy Song Dev++, so I apologize about that.
And then I misspelled Dev++.
So anyway, I'll let you guys take a look at this and give you a few minutes, and you can do that while I sort of talk off the cuff a little bit.
How about that price, guys?
Like, It's above 7,000 now.
I was joking with people yesterday that the market is responding to more developers coming into the ecosystem, which is always a good sign.
And somebody said, well, you know, in acquihires, each developer is worth like $250K.
So each one of you is adding value to the Bitcoin network, hopefully at a rate greater than $250,000.
Anyway, yeah, Lots of stuff to do today.
If you haven't gotten a chance to do this, it's best if you can follow this along and clone this repository and go through some of the Jupyter notebook stuff that I've set up for you.
But yeah, that repo has everything you need not only for my session, but also for John Newberry's session in the afternoon.
That's why we moved it from Jimmy Song to Bitcoin Edge.
And he's been putting pull requests into Bitcoin Edge.
So it's important that you get this particular repo and not that one.
Anyway, here's how you do it.
Go clone it, make sure Python 3, Virtualenv, and Git are installed obviously.
Clone it, then go into the dev++ and start a virtualenv with Python 3 and not something lower like Python 2 and then activate it and then you can install the requirements and then you can go to Jupyter Notebook.
Anyway, let me just give you a short expectation here.

## Class Structure

First of all, here's what we're going to do.
I'm going to present you some material about elliptic curves or finite fields or transaction structure or something.
And then I will give you a chance to ask some questions.
And you're going to have some time to play with or study the code.
Actually, I think the last two are backwards.
You're going to have some time to study some code.
I wrote some very readable Python that if you took my other class, Programming Blockchain, we built.
And basically, you can go look at what the code does.
And we're going to start very basic.
We're going to start from the very basic crypto primitives like finite fields elliptic curves and then we're going to move on to elliptic curve cryptography we're gonna we're going I'm going to attempt to teach you how the curves work and how that produces public key cryptography, because that's at the heart of Bitcoin, right?
Like transactions depend on the ability to sign and verify.
And then we'll talk about transactions, script and two particular types of script, pay to pubkey hash and pay to script hash.
So all of that will be covered in the next three hours or so.
I promise I'll give you some breaks, so don't be horrified at the prospect of staying here for three hours straight.
If you want some water or oranges or something, please just grab a little bit.
There's water up here, some food over here.
And I won't be offended if you just get up, grab something to eat and then come back, go back to your seats, totally fine.
And yeah, if you have any questions or something, just please raise your hand and you know, speak loudly enough that other people can hear you.
And obviously, help everybody out by doing that.

## What We'll Cover

All right, so here's what we're going to cover for the next three hours.
We are going to cover foundational math.
OK?
I'll describe that to you in a bit.
We're going to then go into elliptic curve cryptography, and then we're going to study transactions.
And that's sort of going to be roughly an hour each.
All right, so we're going to start with something called finite fields.
And finite fields are a mathematical structure.

## What Is a Finite Field?

And, you know, I'll describe it to you right here.
What is a finite field?
Well, it's a set of numbers.
It's a set of numbers.
That's really all it is, and it has certain properties.
And it's obviously finite, not infinite, right?
Like the set of all real numbers is infinite, the set of all natural numbers is infinite.
But finite fields, in this particular case, it's finite.
And that's a very important property, because it limits sort of the universe of all things that can possibly be.
And there are four operations in a finite field, addition, subtraction, multiplication, and division, except division by zero.
Note that these are all operations we are going to define.
They aren't necessarily going to jive with your intuition.
You may know addition as like five plus 15 is 20, and you'll see later that's not exactly right in a finite field.
Okay the only exception is division by zero.
Closed means that if you if you take two elements and add them the result is also in the finite field.
Or subtract, or multiply, or divide.
You may be thinking, okay, well, division's kind of weird, because you have all these very small numbers or fractions.
Well, we're gonna have to define division in such a way as to be within that finite field.
And it's mostly used for elliptic curves for cryptography.
It's used for a lot of other things as well, as far as mathematical structures go.
But we're going to study finite fields first, then we're going to study elliptic curves, and then we're going to combine them, and that's where we're going to get the magic of elliptic curve cryptography.
All right, and it turns out prime fields are the most interesting, And by prime fields, I mean that there are a prime number of elements in the field.
So it's a set of numbers, so when you have a prime number of those, it turns out to be really interesting.

## Example Prime Field of 19 (Denoted F)

So here's an example.
Here's the prime field of 19.
It's denoted with an F with a subscript of 19.
And this is what it looks like.
We're gonna call the 19 elements of it zero through 18.
There are exactly 19 elements in a prime field and That's what it looks like.
You can have other prime fields like F97.
It's zero to 96.
And you can have even much larger numbers, right?
48,947 is a prime number.
And a prime field of 48,947 is just zero to 48,946.
So that's what a prime field is.

## Modular Arithmetic

All right, so before we move on to actual operations, I wanna remind you of something that you might have learned a long time ago, and that's modular arithmetic.
Okay, some people call it wrap around math, some people call it remainder math, but it's pretty similar, right?
Like simple, you remember in elementary school when you did division problems like, what's 11 divided by seven?
And then you go, okay, well, there's one, and the remainder is four.
What we're doing is we're just taking the remainder, okay?
The remainder is the modular arithmetic.
You can do the same with 38 divided by 12.
There's three, and then a remainder of two.
And if it helps you visually, just think about a clock.
Yeah?
Sorry, I just want to correct the previous slide where the prime fields, there was an 18 and a 26, so the fields are not solely the prime number.
No, the field is every number up to 26.
Yeah, 0, 1, 2, 3, all the way up to 18, right?
1 minus the prime number.
Okay, all right, so if you think about the clock, right?
And you go, okay, what hour is going to be 38 hours from now?
That's what modulo arithmetic is.
So you'll say, OK, it's 2.
So that's how you can sort of think about it.

## Addition and Subtraction

All right, So let's talk a little bit about how we're going to define addition and subtraction in this field.
And it's going to be exactly the same as modular arithmetic.
So for example, if you have 11 plus 6, that's going to be 17.
17 mod 19 is 17, right?
Like it's like normal addition, like the addition that you are normally used to.
17 minus six is 11.
Again, that's the same intuitive understanding that you might have of subtraction.
When you get above 19 though, that's when your intuition might go a little bit awry, although with addition and subtraction it's not as hard.
Eight plus 14 is 22, mod 19 is three.
So eight plus 14 is three in this particular prime field.
Okay, eight plus 14 is three.
Okay, and note that three is within zero to 18.
So it's within that prime field.
That's how it makes it close.
And you can do the same thing.
Four minus 12 is negative eight.
Negative eight mod 19 is actually 11.
Okay, so four minus 12 is 11, right?
Like that's again a little bit counterintuitive, but that's what we have.
And you know, if the negative number confuses you, just think about adding 19 until you're within the range 0 to 18, and that's it.
All right, so that's addition and subtraction.

## Multiplication and Exponentiation

We can also do multiplication and exponentiation.
Again, same as modular arithmetic.
So two times four is eight, that's not very interesting because it's sort of the same intuitive understanding of multiplication that you have.
But when you get above 19 or above, that's when your intuitive understanding might change a little bit.
Seven times three is 21.
21 mod 19 is two.
So seven times three is actually two in field arithmetic.
And similar with exponentiation, you could do 11 to the third power, it's actually 1331, mine 19 is actually one, so 11 to the third is one.
Again, a little bit unintuitive, but that's what it is.
And there's a nice Python function that helps you do this.
It's called pow, and it will let you do modulo exponentiation.
So that's 11 to the third power mod 19.
And it's faster than doing it sort of manually.
And for very large numbers, this actually ends up being a very important part.
And finally, division.
And this one is defined as the inverse of multiplication.
So remember how two times four is eight?
That's not very interesting.
So eight divided by four is two.
Okay, easy enough, right?
Here's one that will start challenging your intuition.
Seven times three is two, so two divided by three is seven, because that's the inverse, okay?
So two divided by three is seven, because that's the inverse.
So two divided by three is seven.
Kind of very unintuitive, but that's in fact the case in field division.
Same thing with 15 times four is three.
Three divided by four is 15.
Again, very unintuitive, but field division has sort of elements like that.
And 11 times 11 is seven, seven divided by 11 is 11.
And it's the inverse of multiplication, that's kind of how you have to think about it.
So the question you might have at this point is, well then how do you actually figure out the division?
Right, like how do you analytically get the division?

## Fermat's Little Theorem

Well, for that we require Fermat's little theorem, and this only works with prime fields.
And it's due to his theorem which states this, n to the p minus one equals one mod p.
And this is true for any p that's prime, and any n.
It doesn't matter what the n is as long as it's not zero.
So, works for all n greater than zero if p is prime.
This means that one over n, another way to sort of write that is n to the minus one.
So you, and it turns out you can just add p minus one to the exponent as much as you want because that's equal to one mod p.
So one over n is actually n to the p minus two mod p, which means we can do division.
Okay, we can do division.

## Division So how do we calculate it? (F)

So let's remember, so how do we calculate division?
All right, so n to the p minus one equals one implies that one over n is actually equal to n to the p minus two.
So that means two divided by three is two times one divided by three.
That much should be easy.
But one divided by three is equal to three to the p minus two, which is p is 19, so three to the 17.
And you can actually do this in your Jupyter Notebook or something and check.
Two times three to the 17 mod 19 is actually seven.
And you can analytically calculate it.
But this should also give you some intuition as to why division kind of sucks.
And it's very computing intensive because you're going to have to take it to these enormous numbers when we use much larger primes later.
Again, three divided by 15, we can do the calculation.
Three times one divided by 15 is, you know, three times 15 to the 17th.
15 to the 17th is an enormous number already, and we're using a very small prime.
But we modulo it with 19, and that's equal to 4.
So 3 divided by 15 is 4.
Again, we can use the pow function.
And this will help out in sort of lessening the computational burden on a computer.
It's pow and p minus two p.
It sort of optimizes along the modulo exponentiation.
Anyway, here are some examples.
The library that I have in Dev++ has something called field element and you initialize a field element with the actual number and the prime and you can add, subtract, multiply, exponentiate, and divide, and that's what you can do.
So here's what I want you to do.
Go to your Jupyter notebook, whoops.
Let me move that, all right.
Go to your Jupyter notebook, and this has, this is what it should look like.
It says ECC has a class field element and field element test.
Go take a look at them and you can click on ecc.py, and that has a field element, and it has all of the operations that I described, add, subtract, multiply, RML, something else, but POW and TrueDiv, and you can go study that for like the next few minutes and take a look and see if it matches your intuitive understanding of what we just did.
And I described to you like what the pow function does and all that stuff.
So yeah, take a few minutes.
There are trainers in the room, so if you have questions, you can ask some of them.
But yeah, take a look at it and play with the Jupyter notebook and try to get that going.
Alright, so the transactions.ipynb is where you wanna sort of play with stuff and If you run this, it will sort of show you all the results.
And you can see like, two plus 15 is 17, field of 19, you can, A minus B, yeah, two minus 15 is six, and two times 15 is 11, and all that stuff.
You can just play with it and try different things.
Feel free to play with it, But shift enter, if you don't know Jupyter Notebook, is how you kind of run it again.
And you can change some numbers around, you can make this like 13 and see what happens.
And you get different answers for all of them.
But that's the idea behind utilizing Jupyter Notebook to get more familiar with the concept of finite fields.
All right, so let's move to some questions you might have.
Do you have any questions on finite fields so far?
Do you have any, like, does it make sense to you so far?
Yeah, let's go over division again.
All right, so the key to division is Fermat's little theorem.
Okay, right, it's n to the p minus one is equal to one mod p.
And that means that one over n, which is really n to the minus 1, is equal to n to the p minus 2 mod p.
Stated more simply, it's this.
N to the p minus 1 equals 1 implies that 1 over n is n to the p minus two.
And that's because one over n is the same as n to the negative one.
And we can do division this way by taking one over three and recalculating it as three to the 17th, or three to the p minus two.
Turns out that division is the most expensive operation in field math, and that turns out to be an area where you can optimize quite a bit.
Other questions?
I have a question.
Yeah.
So big picture, how is this all related to Bitcoin?
Yeah, so big picture, we're going to utilize this for elliptic curve cryptography.
And elliptic curve cryptography, specifically ECDSA, is what is used to secure every transaction.
So this is the primitive that you need in order to understand ECDSA and you need to understand ECDSA to understand actual transactions and you need to understand transactions to learn about blocks and everything else.
Transactions are sort of at the heart of Bitcoin.
And, you know, ECDSA is at the heart of a transaction.
And finite fields and elliptic curves are just something you have to learn in order to understand ECDSA.
All right, any other questions?
Yeah?
When I'm doing two divide by three, what's n and what's p?
Yeah, so n in that instance is going to be three, right?
N is three because you're dividing one divided by three.
And P in this case is the prime of the field.
P stands for prime, so 19.
So 19 minus two is 17, so it's three to the 17 is the same as 1 divided by 3.
Other questions?
All right, let's move on then.
All right, we're going to talk a little bit about elliptic curves.
And we'll go over what the equations are and stuff, but I wanna sort of start from a place of talking about what you might have seen in high school.
So think about graphing, right?
Like you guys Remember this graph?
So what is it called?
Yeah, a line, it's a line, right?
And it's y equals mx plus b.
You probably learned this in like seventh grade or something.
And m is the slope and b is the y intercept.
And it's a very simple line.
And the equation is y equals ax plus b.
All right, who remembers this?
Okay, you guys remember the quadratic formula, right?
Like this is a parabola And this is y equals ax squared plus bx plus c.
Okay, pretty, you guys should be fairly familiar with that.
All right, who remembers this?
This may be like 10th grade, I don't know.
It's, this is a cubic, right?
Like it's kind of like an inverted parabola a little bit.
Anyway, an elliptic curve is actually not that different.
It's y squared equals x cubed plus bx plus C.
And the big difference between this and the previous one, cubic, is that at least the top half looks very similar to what a cubic would look like.
The top half looks very similar to a cubic, except it's a little flatter.
And the bottom half is just a reflection of the top half because of the y squared term on the left.
So if y is a solution, then negative y will be a solution.
But typically this is what an elliptic curve will look like.
All right, so that's an elliptic curve.
So here's the curve used by Bitcoin, SCCP256K1, and it's y squared equals x cubed plus seven.
This is the curve.
And it's actually, you know, that's what the curve looks like over a real line.

## Point Addition

All right, the key thing about an elliptic curve that somebody discovered is something called point addition and we don't have time to get into the exact specifics of it, but it turns out if a line intersects an elliptic curve at two points, it will intersect a third time.
If a line intersects an elliptic curve at two points, it will intersect a third time.
And this is true of any line that intersects the curve.
So, I mean, it can be tangent to it, in which case it's a little different.
But the only exception is if points are exactly opposite of each other.
And you can sort of see it with R and P plus G, right?
Like they're exactly opposite, and it goes all the way to the, you know, it can't intersect anywhere else.
It'll go to infinity on both sides.
But that's what point addition is.
It's, you find the third point that it intersects and you reflect over the x-axis and that's how we define point addition, okay?
That's point addition.
All right, so It turns out that we need that point at it.
We define sort of a point at infinity to intersect with two points that will intersect a third time, like two points that are exactly opposite each other, like R and P plus Q in this example.
And we add that third point, a point at infinity, so that it will intersect the curve a third time.
Right?

## Group Law for the point at

Like that's, and we do that for a very specific reason.
But anyway, there's something called the group law for the point at infinity.
And you can, we're, we're defining sort of like point addition, adding points together, right?
And we're going to sort of define addition with this in mind.
So if you add any point, add the point at infinity to any point, it comes back to the same point.
And if you add the point and its opposite, then it's going to come out to the point at infinity.
So think zero as far as the point at infinity goes.
As far as point addition is concerned, the point at infinity acts a lot like zero.
Here's the group law for x1 is not equal to x2.
And this is finding the third point.
And this hopefully will give you some intuition.
In order to find the third point that you intersect with, you need to sort of figure out the slope and then find out where it intersects and then get the point opposite.
So we define point addition, x1y1 plus x2y2 is x3y3.
And in order to do that, we first find a slope.
You guys remember slope from like seventh grade, right?
It's a change in y over change in x, and this is why it's important that x1 is not equal to x2, because if the x1 were equal to x2, then this slope would be zero.
The denominator for the slope would be zero.
X3 equals slope squared plus minus x1 minus x2.
We can derive this based on the equations, but I won't do that right now.
And y3 is equal to slope times x1 minus x3 minus y1.
This is just the formula, and we can derive it using the elliptic curve equation and the line equation and figure out the third point that it intersects.
All right, so here's an example.
We have a curve.
I'm going to purposely define a different curve than Bitcoin.
Y squared equals x cubed plus 5x plus 7.
So we want to find out 2, 5 plus 3, 7.
So we can prove that 2, 5 is on this curve because what's 2 to the third plus 2 times 5 plus 7?
Can anyone do it in their head?
So 2 to the 3rd plus 2 times 5 plus 7.
25 right?
And what's 5 squared?
25 yeah.
So it's it's 25 on both sides.
All right You can do the same thing with 3, 7.
I'll leave that to you as an exercise.
But we find the slope first, right?
The s equals this thing.
And the slope is 2.
And then we can figure out what x3 is and y3 is, and we get the answer.
2, 5 plus 3, 7 is negative 1, 1.
And this is how we sort of work with elliptic curve point addition.
Now, what if the points are the same, right?
Group law for x1 equals x2 and y1 equals y2.
Well, then we have to find the slope and it's actually the point that's tangent to the curve.
And in order to do that, well, so we're defining it as like sort of this thing.
We have to find a slope, and this is from calculus, maybe like 12th grade for many of you.
You find the derivative of x and the derivative of y, So that's where you get 3x1 squared plus a and 2y1.
That's the derivative of the right side over the derivative of the left side.
Anyway, the x3 formula and the y3 formula remain the same.
Just the x1's are equal, so you can make it that way.

## Examples

Anyway, here's the example.
We can create these points.
In ecc.py, there's a class called point that you can go study.
But basically, if x is none and y is none, we call that the point in infinity.
So think of p0 as literally 0.
And p1 is one of the points on the curve y squared equals x cubed plus 5x plus 7.
That's what the a and b are, is the coefficient in front of x and the last constant, and p2.
And you can do different things with it.
You can add, subtract, whatever.
Well, you can only add right now actually.
Yeah, no, adding is the only thing that you can do.
But check it out and you'll notice something.
There's no real pattern to point addition, right?
Sometimes it'll be like the x and y coordinates will be way less, sometimes it'll be way more.
And it's highly, highly nonlinear.
And that's part of the property that we're taking advantage of with respect to ECDSA, which we'll study in a bit.
But anyway, please study these two things, ask questions afterwards, and and you know I'll be coming around and seeing how you're doing.
Anyway, the main function that you're going to want to look at is add.
It does like when x is not equal to, x1 is not equal to x2, and when x1 equals x2, and when one of them is the point at infinity.
Those are the main ones that you'll want to look at.
All right, so let's take some questions on elliptic curves.
Any questions?
Any questions?
Yeah?
Or like a high level of what addition is for?
Is there an easy way to find like, what it's gonna be used for?
Yeah, so the fact that it's highly nonlinear is going to come in very, very useful in the next section.
So it turns out for elliptic curve cryptography, Oh, well, yeah, I gotta press continue.
Yeah, it turns out for elliptic curve cryptography, it's highly nonlinear nature makes it very hard to predict where it's going to end up.
And we're going to combine finite fields and elliptic curves.
And when you do that, you have a finite set that's extremely hard to predict where it's going to go.
And that's at the heart of elliptic curve cryptography.
Yeah.
This is the foundation of SHA 256 hash, right?
No, no, This is a foundation of ECDSA.
So elliptic curve cryptography, it's for signing and verification, not hashing.
Hashing is something different.
Yeah.
Yeah.
Were you talking about the point at infinity?
Uh-huh.
That's the area predicted on the curve?
I'm not sure.
But basically, you need to define a point at infinity in order for the map to work out for point addition.
Yeah.
Can you describe the intuition behind calculating the y coordinate from the sum?
The y coordinate from the sum?
You can, there's no real intuition for it, except that if you plug in the formula for a line and plug in the equation, that's what you end up with for y, yeah, as the third point.
Any other questions?
All right, let's get into the magic.
So I'm sort of feeding you vegetables right now, but I promise you this is going to have a payoff here.
Elliptic curves over finite fields, okay?
So you can combine the two concepts.
You can take an elliptic curve and you can do it over a finite field.

## Elliptic Curve over Reals

So here's elliptic curve over reals.
That's, that's, it looks like a nice smooth curve.
It looks great.

## Elliptic Curve over Finite Field

You do it over a finite field that looks like a complete scatter shot, okay?
That's what it looks like.
And that's okay, because it turns out all of the equations still go through.
All of the equations for the elliptic curve go through in a finite field.
And what that causes is that we have a finite number of points in it and we can do the same math.
So here's an example.
So you could create a finite field element, and A and B, and they're over the prime 137, which I chose for some reason.
And you could create these points, right?
Like you can still create the point at infinity, that's going to be none and none.
Point one is a finite field, I mean, it's a point over a finite field.
The x is field element 73, 137.
Y is finite field element 128, 137.
And you can do the same.
And you can prove that all the equations from the elliptic curve, like y squared equals x cubed plus 7, which is the one for Bitcoin, which is what we're using here, those numbers will go through with the finite field math.
You did the squaring, you did the multiplying, you did the division, all that stuff.
All of those equations still go through for the elliptic curve.
And that's where we kind of get a lot of that magic.
And you could try some of it.
So Take a look at this real quick.
This is ECC test, test on curve and test add one.
We're defining some of the, Yeah, ECC test.
It basically, we just combine the two concepts.
We combine finite fields and elliptic curves.
Where instead of using real or normal numbers, we're using finite field elements into the same equations.
And they all go through, which is really crazy, but that's kind of how math works sometimes.
Like you have a finite field and you can plug in the same stuff into all of these equations, but because we define them a certain way, they all go through.
So take a look, try it on your Jupyter notebook.
Yeah, try it on your Jupyter notebook.
I think it's, yeah, elliptic curves over finite fields.
And you can try it, and you'll get like point addition with over a finite field.
So you could try a lot of different things.
And The key though is that these numbers have to fit the equation.
So x and y, so it's y squared equals x cubed plus 7, and it has to resolve in the field math.
And that's how I found these points is 73, 128 will satisfy that equation.
And certainly the result will satisfy that equation, but you'll need to do certain things.
You can't just put in any random numbers there.
All right, any questions regarding like elliptic curves over finite fields?
This is combining two concepts, yeah.
Is there a reason why you don't check the prime for having the number?
Which number?
The number to prime.
Oh yeah, I just didn't code that I guess that's that's about the only reason yeah.
Yeah, so a line in a finite field is kind of a tricky concept.
It's not like over a real number line, like it looks like a line.
It doesn't look like a line over a finite field.
So it's, I think if you wrap it around it might, but it goes all over the place because you have to continue it.
It's not, it'll sort of go off one end of the map and come back on the other side depending on like because it's Wrap-around map on both sides and it will eventually hit that point, but it'll come close on all the other points So it's it's hard to sort of visualize that way Yeah Yeah, they the finite fields basic more or less represent integers.
And when you do it that way, that's what, it looks like this.
There's no real, it's hard to make an intuition about it because it's not smooth.
Any other questions?
All right, let's move on.
All right, so turns out that we can make something called a mathematical group out of this.

## Mathematical Group • Single operation

And a mathematical group is a single operation.
It's closed if A, B is in G, then A plus B is in G and plus is the operation we'll call it.
It's associative, It's commutative, this might be familiar to you.
It's invertible, and it's got an identity.
And it turns out that point addition gets us a group.
Point addition gets us a group.
So you can kind of see that it's closed, right?
If you intersect at two points, you'll intersect at a third point.
It's commutative, P plus Q is the same as Q plus P because you still end up intersecting at the same third point.
And it's invertible because whatever is on the opposite side, right?
If you take the same point and do the opposite side of the x-axis, reflect it over the x-axis, that's the negative number.

## Associative

It's also associative, And this is a little bit, you're gonna have to trust the graph on this one.
There's no real easy intuition for this.
But if you add A and B, you come up with that point at the bottom here, right, A plus B.
And then you add C to it and you end up at this point.
If you add B plus C first, you end up at that point B plus C.
And then you add A to it and you end up at the same point essentially.
It doesn't matter which order you add them.
And that's part of why you need to reflect over the x-axis.
It ends up satisfying this property.
Kind of random, but that's how it works sometimes.

## Scalar Multiplication Start with an Elliptic Curve over a Finite Field.

So we could do something called scalar multiplication.
And we start with an elliptic curve over a finite field and just pick a random point, any point, okay?
Some random point.
And then we keep adding to that generator point, the same, we can add that point, and then we have something called 2G, and then we can add G again, and we have 3G and so on, because of associativity, doesn't matter which order you add them, until we get to the point at infinity.
And that gets us a finite group.
And that finite group is highly, highly nonlinear.
So here's sort of like some code to sort of see that a little bit.
You have a field element, you have a point, and you keep adding to that point, that while loop at the bottom.
We keep adding to that point until we get the point at infinity.
And it turns out that we need to add it to itself 69 times before we get the point at infinity.
So that's what the RML thing is about.
So take a look at it.
Please take a look at that one, it is arm-all.
And it sort of shows a bunch of ways in which you can combine a point with itself, you add the point to itself, and that's what we call sort of scalar multiplication.
And the code is in ecc.py still, so you can go take a look at that.
We already have that open, don't we?
Oh yeah.
RML, yeah, so.
Oh yeah.
RMO, yeah, so.
We are very close to defining secpig256k1.
So all right, so any questions on this?
Yeah.
So you have the while loop in order to figure out its convergence on infinity or zero, right?
Uh-huh.
Is there any other way that you can emphasize like the root force?
Like is there like- There is.
And we'll, we'll talk about it's in the code later with S256, but it's a short, short preview.
It's called binary expansion.
So you keep doubling it, and even if it's a very, very large number, you can get to it by doubling it many, many times.
You take a number and it's a binary representation, and you only add if there's a one in that One in it, so that's something that you could take a look at in the code in a bit any other questions All right great, let's talk about scalar Multiplication all right, So we've been so far doing everything over a relatively small prime, like 137, 19, or whatever.

## Scalar Multiplication Imagine a really large group n-2256

Imagine a much, much larger group, 2 to the 256.
And imagine P equals SG, where S is really, really large, right?
In the, on the order of 2 to the 256.
Finding P when we know S is easy.
We just we just add you know, we do the binary expansion thing like I just mentioned, and we can add enough, we can sort of figure out where it's gonna end up.
But, finding S when we know P is not, okay?
We can't figure out, okay, what did we have to multiply?
And this has to do with the highly non-linear nature of elliptic of point addition.
Okay it might be less it might be more it's it's really hard to tell where it's going to go.
And And this is sometimes referred to as the secret exponent and if you, instead of using addition as the operator, if you use multiplication as the operator, it looks like P equals G to the S and you invert that and that's log G P equals s and this is called the discrete log problem and it's as hard as factoring a very large composite number with two very large primes.
So conventionally we use little s for secret or scalar or something like that and uppercase P for public point or something to that effect.

## Defining an Elliptic Curve • Elliptic Curve Equation (a and b of y=x+ax+b)

And that's kind of how we define an elliptic curve.
We have the elliptic curve equation, y squared equals x cubed plus ax plus b.
We have the finite field prime number, p.
We have the generator point, some g, okay?
We just sort of pick a random one with a high order.
And the number of points in that group, n, that sort of defines an elliptic curve.
And SecP256K1, this is the curve used in Bitcoin, has this equation, y squared equals x cubed plus 7, where a is 0 and b is 7, right?
And the prime field is a very large prime number, 2 to the 256 minus 2 to the 32nd minus 977.
That is a prime number.
And a generator point, some random point basically, and it looks kind of random for that reason.
And the order n.
It turns out that most of the points in this elliptic curve over a finite field are in this group, almost all of them.
And it's actually a very small number that are not.
And by the way, SEC stands for Standards for Efficient Cryptography.
That's where the SEC part of SEC P256K1 comes from.
And 256, that's the number of bits in the prime field.
So it's raised to 2 to the 256, so that's why it has 256 in the name.
So if you see other curves like SEC P384, something like that, the 384 just stands for the number of bits in the prime field.
Alright so I just want to impress upon you the fact that 2 to the 256 is a really really really big number okay it's roughly 10 to the 77th power.
And the number of atoms in and on Earth is about 10 to the 50th number of atoms.
Number of atoms in the solar system, not much bigger, 10 to the 57th.
Number of atoms in the galaxy, 10 to the 68th.
We are still nowhere near Turns out you need to go to the number of atoms in the universe to actually overtake it 10 to the 80th.
Okay insane Insanely large number yet.
It's expressible in just 32 bytes Just to give you an idea of trying to brute force attack this, a trillion computers doing a trillion operations every one trillionth of a second for a trillion years will still do less than 10 to the 56 operations.
So you're still nowhere near brute forcing this thing at 10 to the 56.
And that's a trillion years of a trillion computers.
And you know, trillion's barely at the edge of our like cognitive ability to think about, But it's a really, really big number.

## Public Key Cryptography

All right, so here's how we do public key cryptography.
The private key is the scaler for a generator point.
So we're doing lots of point addition against itself over a finite field.
And the public key is the resulting point, SG, right?
Like it's really just the two numbers, the X and the Y coordinate for that point.
So it's really two numbers.
So the scalar is one 256-bit number, And the public key is two 256-bit numbers And really when you have a Bitcoin private key, it's just that that scaler It's some 256-bit number all that All of the securing that you're doing, it's really to secure one 256-bit number or something that can be stored in just 32 bytes.
Which is kind of crazy, because to generate that particular 32 bytes thing is going to take way more than the age of the universe to compute by brute force.

## Getting a public key from private

But anyway, here's how you get the public key from private.
If you look at ecc.py, There's a generator point G that I've made and a couple of other classes, S256 field and S256 point.
And those basically hard code the prime that's in SCCP256K1.
But anyway, here's how you do it.
Here's the secret, 999.
That's a terrible secret.
Don't ever use it.
A lot of brain wallets kind of work this way where it basically encodes your word into some number.
But that's essentially what they're doing.
But this is easily brute forcible.
You can go through a thousand.
Point is secret times G, and that's scalar multiplication.
And you can look at the point.
Well, here's this sort of random looking point.
There's no real pattern to it.
But that's what you would hand out to other people, and you can encode stuff with your secret.
Anyway, take a look at s256 field and s256 point it it has a lot of the constants that I showed you and it's combining an elliptic curve over a finite field yeah take a look at it please feel to ask me questions or ask your neighbor that understands better or possibly some of the trainers.
All right, so any questions on this part, the SecP256K1 curve and what you're doing with it?
Because this is at the heart of everything, right?
All right, so let's move on.
Here are Bitcoin addresses and how they're related to what we've been studying.
So the SEC format is standards for efficient cryptography, again, and think about a public key.
It's a point on the curve, right?
It's got an X coordinate and a Y coordinate, and you need to serialize that in some way, right?
You need to put that on disk in some way.
And the SEC format has two versions, uncompressed, which looks like this.
And that's, you have a zero four as a marker, and then you put the x coordinate and 32 bytes as like base 256 I guess, and as the first part, and then the y coordinate.
So it's x coordinate, zero four x coordinate, y coordinate.
That's what the SCC format is.
The compressed version, and this by the way was what Satoshi used very early on in the early transactions.
He used all on compressed keys and in fact compressed keys didn't come into effect until much later.
It's hypothesized that Satoshi didn't know about compressed keys.
But this is 65 bytes, and this is before Bitcoin addresses were a thing, he would send the 65 bytes to whoever wanted to pay him, or him or her, or they, whatever, pay Satoshi.
And that's what would have happened.
All right, compressed looks a little different.
So it looks like that.
And you can tell, first of all, it's much shorter, right?
It's only 33 bytes instead of 65.
And the first marker is 0, 2 if y is even, and 0, 3 if it's odd.
Remember, for any x, there are two y's, only two y's that can happen.
And there are negatives of each other, but in a finite field that's prime, the negative of an odd one will be even, and the negative of an even one will be odd, because it's a prime number, and prime numbers greater than two are odd.
So anyway, so it starts with a zero two if y is even, zero three if y is odd, and then you just add the x coordinate.
That's why it's able to be much smaller because it's a compressed, and why it's called a compressed key, because you're not spelling out y for the other person.
And that's the SCC format.
Addresses are, I mean, so SCC format is really encoding a point on the curve, right?
An X, Y coordinate on the curve.

## Addresses • Take either compressed or uncompressed SEC format

And once you've encoded that, this is how you generate an address.
You take either the compressed or uncompressed SCC format, you shot 256 and write the MD160, the result, we'll get to exactly why later.
And that's called the hash 160 in Bitcoin parlance.
We're hashing this thing in some particular way.
And then we prepend the network prefix, as 00 for mainnet, 6F for testnet.
Litecoin uses some other prefix, other coins use other prefixes, but this is how you sort of identify it's supposed to be for Bitcoin.
And then add a 32-bit double-shot 256 checksum to the end.
And that's a way to make sure that the address is not transmitted badly by saying something bad.
And then it's encoded in base 58 and that's a way to make it human readable.
So the example is here, I'm using the same terrible secret, 999, and you can look at the various versions.
So every private key actually has like two Bitcoin addresses that you can generate out of it because you can use the uncompressed SEC format and the compressed SEC format.

## Study ecc.py: S256Test

And obviously for testnet it's going to be a little different, but take a look at the s256 test And you can take a look at what's going on Let's see back here Yeah, so if you run this one, you'll get, you know, like, addresses that look like Bitcoin addresses that start with a 1.
The testnet ones start with an M or an N, and that's because of the poorly chosen prefix.
But yeah, take a look at that, study it a little bit, and see, you know, just look at how it's constructed, because that's how you get a Bitcoin address from a public key.
All right, we'll do the next section and then we'll take a break, just so you have some light at the end of the tunnel here.
All right, any questions on the, you know, SecP256 test or, you know, what we just covered?
Okay, I think a lot of you, yeah.
When you talk about the compressed form, you talk about all the, and even numbers.
Okay, yeah.
I know that it needs to represent two numbers, one odd and one even.
But why?
Why odd and even?
Yeah, So if one number is even, right, and you take the negative of that, in a prime field, that means that the other one will be odd.
So they're never going to be both even or both odd.
One has to be even and one's odd.
And so that's how you can kind of tell.
That's one way to classify it basically.
So think about, so the field is prime, so And a prime number greater than two is odd, right?
And those two y's have to add up to the sum of the prime field.
So that's why.
Does that make sense?
If one is even, the other has to be odd.
And if one is odd, the other has to be even.
Just an effective way to compress it.
Any other questions?
I don't know if I explained that well.
Yeah?
Small question, because on the SQ56 address, why in the left line do you show this and basically do you also need to be able to ask?
Oh, Let's see, that's a good question.
This is what line?
347?
377.
Yeah, so I'm doing that to return it as a string.
This is like a Python three thing.
It otherwise will return it as bytes instead of a string.
And I want, like it's supposed to be human readable.
It should be a string, yeah.
But you don't have to do that.
It'll return just as bytes.
And that looks fine.
Yeah, the B, B, B, B, it removes the B quote, yeah.
Anything else?
Alright, let's get to the actual signature algorithm and how you can use these secrets and pubkeys in order to actually sign stuff.

## Intuition

All right, so I wanna give you an intuition for this first.
So we know this, SG equals P.
This is sort of the main formula here.
S is the secret, right?
That's the private key.
P is the public key.
This is what you share with everybody and I want to I want you to take a look at that that equation UG plus VP where U and V are not zero, so there's some quantity of both.
And I want to convince you or give you some intuition that this is impossible to manipulate unless you know how G and P are related.
If you know how G and P are related, you can do things with it.
If you don't know how they're related, you end up with some random point.
So say you can choose UNV.
You can only manipulate the sum if you know how GMP are related.
And really, the way they're related is with the secret.
So if you know the secret, you can manipulate things.
If you don't know the secret, you can't manipulate things.
Okay?
If you don't know the secret, this is gonna end up sort of as a random point on the curve.
If you know the secret, you can sort of manipulate things so that it ends up being something that you can make into something.
So if you do know the secret, then UG plus VP equals UG plus VSG, okay?
P is SG, so you just substitute that and that's what you get.
And you can factor out G from both of them and you get U plus SV.
So you can sort of manipulate that quantity if you know the secret versus when you don't.

## Signature Algorithm

And that's kind of the basis for the signature and verification algorithm.
You first start with a hash of what you're signing.
You're going to sign something, right?
Like here's the check that you're actually going to sign.
Then you assume, next assume your secret is E, and we don't use S here as the variable name because it turns out that S is used later as part of the signature.
So P equals EG.
Next, get a new random number K.
Okay, and we are going to compute KG, okay?
And you have an X and Y coordinate from the resulting point.
We're just going to look at the X coordinate and we're gonna call that R.
Okay, R.
And we're going to compute S.
And S is going to be Z plus RE over K, and division is the same as field division, except with N instead of P.
And we can do that.
And the signer can compute S since he has the secret E.
Nobody else can compute S.
And the signature is simply the pair R, which was more or less randomly generated, right?
Because you chose a new random number K to get that R.
And S, which is sort of like proof that you have this secret.
And that's computed using this.
And the way you verify, oh, S has to be less, and this is a malleability thing that they implemented.
This is like called the strict-dir signature.
But S has to be less than N divided by two.
If not, you have to use n minus s, but this small implementation detail.
Anyway, the verification algorithm, again, starts with the hash of whatever it is that was signed, right, it's whatever the check was or whatever, and you have the public point because that's shared with the public, so you have P.
And you have the signature R comma S, where S is this quantity.
And you can compute U, Z divided by S, and V, R divided by S.
And you compute UG plus VP.
This is the intuition I gave you earlier.
You can only manipulate this if you know how G and P are related, otherwise there's going to be some random point on the curve.
And we can expand this out.
UG plus VP, U is defined as Z divided by S, and V is defined as R divided by S, and P is of course E times G, and you can factor out G, and you get z plus re divided by s, and s was defined as z plus re over k.
So you factor all that out, and we end up with kg, which you remember K was randomly chosen and the X coordinate is R.
So a lot of like signature and verification algorithms kind of are like this where you start with a number and you end with the same number.
You're sort of like closing the loop.
You start with R and you end with R, right?
And if the X coordinate matches R, you have a valid sig.
And this is sort of characteristic of non-interactive proofs of one kind or another, is that you start with some random number and you can end with the same random number.
Okay?
And this proves that, you know, the person that created the signature knew the secret.
And that's the essence of it, is that you don't need to know the, you never use E as part of the verification algorithm.
You just, you calculate U and V and then calculate this quantity and you end up with the x coordinate the same as what you started with.
Anyway, here's an example.
I chose some random z.
This is like the hash that you're assigning, interpreted as a number.
Again, we're using the same terrible secret.
And we're going to make this private key, and we have the pub key, priv key dot point.
You can take a look at the private key class in ecc.py.
And We're going to sign with sign Z, which is the hash that we're signing.
We're going to print the signature and we're going to verify the signature and it turns out that the signature is valid.
Anyway, study these And then after this we'll take a break.
Yeah, study these, ask me questions, then we'll take a break.
All right, so any questions on this stuff?
Yes.
Yeah.
So inside why S has to be less than half N?
Oh yeah, So why does S have to be less than half N?
Oh yeah, so why does S have to be less than half N?
That's a malleability vector.
So it turned out that what people were doing to malleate transactions was change the signature so that the S part was N minus S and that would give two versions of the same transaction and they wanted to eliminate that vector.
If you substitute it with N minus S, it turns out all the signatures go through and everything.
But you don't want two versions of the same transaction.
So they said, okay, we're just gonna always use the lower one.
And upper ones are still valid on the blockchain, but they're not gonna get relayed.
So that's what that was.
Actually, BIP-66, I don't know.
John, do you know?
If BIP-66 enforces the half-N rule?
Okay, I guess we'll have to take a look later.
Any other questions?
Yeah.
You said non-interactive proof.
What is that?
All right, so a normal interactive proof is where I can check.
Like, if you had the private key and I were trying to find out if you had the private key, I would give you a challenge and I would say, here's something I want you to sign.
And then you sign it and then you give it back to me.
That's interactive, right, because it requires a round trip.
A non-interactive proof means that I construct a proof without your involvement.
And those tend to be really useful, a lot more useful actually than interactive proofs.
So that's what we do with this.
By the way, there's something called deterministic signatures where that random number K and R subsequently is generated by something as part of the transaction.
But yeah, it's a way to sort of reduce malleability even more.
Any other questions?
Yeah.
You said, short the proof without knowing is that just like the idea of signing?
Yeah, it's the idea of signing with a private key without getting any input from anybody else.
So you're generating all the entropy or randomness in there.
And you still prove it by sort of coming back full circle with this.
You start with R and you end with R.
And you can't do that if you don't have the secret.
And that ends up being a very good property.
And that's different because like, even though I'm still signing something, I'm gonna send a message, like the challenge is that I'm still interacting.
Yeah, so the interactive ones tend to be very annoying, because both people have to be online.
And, you know, I mean, that's more feasible when for something like lightning network or something.
I don't think they use interactive proofs, but if they wanted to, they could.
With something like Bitcoin, you need to sort of sign something and let it be out there.
And instead of everybody that wants to verify issuing you a challenge and proving it, that would be way too crazy.
Any other questions?
Yeah.
What does it mean to sign?
What does it mean to sign?
You're saying that your algorithm says start with a hash of what you're signing.
Yeah, so start with a hash of what you're signing.
So it's like, what's the check?
Right, like in Bitcoin parlance, if you think of transactions as like checks, right?
Like I'm signing over five Bitcoins to you or something like that.
That's the check.
You need to sign that check or else it's not valid.
And you need the check to sign first and that's kind of what the Z is, that's the hash to sign.
Yeah.
Yeah.
Having the private key and calling it in different ways, these calls are different signals.
Wait, you said something about different private keys?
Sorry.
So the private key is the same.
Oh, so compressed versus uncompressed, yeah.
So that would be the public point yeah.
That would be so you can have two different addresses for the same public point and the same private key.
But as far as the signature, that wouldn't change necessarily.
You would just have like a different R or something like that because you choose a random point as part of it.
The private point is always represented the same way?
The private point?
The private key.
Is represented in the same way?
Well, there's something called WIF format, and that's the wallet import format, which I don't know if I'm getting to.
But basically, it's a way to encode the 256 bits.
Again, your private key is just a number.
It's a 256-bit number.
And there's something called wallet import format that's human readable.
It's a lot like Bitcoin addresses.
And uncompressed ones start with a five.
Compressed ones start with like an L or a K.
And that's that you might see it very rarely some some wallets allow you to export it But that's usually how you serialize private keys.
Most of you are at least somewhat familiar with Bitcoin.
And Bitcoin has something called a blockchain, and it's just a really giant ledger.
And you need to assign one, once, you know, some Bitcoin from one person to another.
This is how you do it.
You create a transaction.
Addresses, as we know them, the ones that start with a one or a three or whatever, they are really compressed scripts, and we'll get to exactly what a script means in a bit.
But here's what a Bitcoin transaction looks like.
It has something called version.
It's four bytes.
It has inputs, some number of inputs, some number of outputs, and then something called lock time.
And we'll go through what all of those mean.
But inputs, there are two types of inputs.
There are coin-based inputs.
These are newly generated coins that block, you know, miners can create as part of a block, or a previous transaction output.
It's something else that hasn't been spent yet, some output that hasn't been spent yet that you're allowed to spend.
Input has various elements.
It has the previous transaction hash, unless it's a coinbase in which that's gonna be all zeros.
And Vout, the output index in that transaction.
So you're spending a specific output of a transaction.
So a transaction may have like 30 outputs or something.
You have to specify which one of those that you're spending.
You have something called sequence, which is sometimes used by RBF or replaced by fee, but not used very often.
And script sig, and this involves a script language, which we'll get to later.
Basically, the big thing to know here is that there's no amount, right?
There's no amount of how much you're getting to spend.
You actually have to go look that up on the blockchain, or you have to have some trusted third party that will tell you what it is.
All nodes have to validate these inputs as legitimate.
So every node looks up this input and says, OK, has it been spent yet?
If not, that means it's OK.
If it already has, then it's an attempt at a double spend.
And if it's a double spend and the transaction's been confirmed already, they're just going to reject it.
And you know, other things related to that.
Output has elements, there's an amount, unlike the input, this actually has an amount.
And a script pub key, and this again involves a script language.
Think of this sort of as an encumbrance, or sort of like a lock that you're putting in.
On the one script, stig, which is in the input, sort of unlocks it.
All right, so what we think of as assigning to an address is actually a script and script pubkey.
And we'll get into exactly what the script language is about, but that's what it is.
And the amount can be zero in certain instances, specifically with op return.
You can add 80 bytes as part of it.
And finally, lock time.
Lock time is designed to tell nodes not to let a certain transaction in until a certain time or a block height.
So if it's less than 500 million, then it's a block number.
If it's greater than 500 million, then it is a block, it's a Unix timestamp.
But it's illegal for that transaction then to go into a block until that time stamp or that block number has passed.
All right, so here's what a Bitcoin transaction looks like and this is the hex dump of a Bitcoin transaction and hopefully I can point out what they are and they're color-coded for a reason.
That first part, the first four bytes is version, okay, and the version for this Bitcoin transaction is one.
And then the red thing afterwards is the number of inputs.
And in this particular transaction, there's only one input.
And then this blue thing is the previous transaction hash.
And this is the double shot 256 of the actual transaction.
So this is 32 bytes.
And then the previous transaction index, or like which output on that transaction you're spending.
And then you have something called the script sig.
Think of this as sort of unlocking that, being allowed to unlock that particular transaction output.
And you have sequence, which is almost always all Fs, or F, E, F, F, F, F, F, F, F.
Not really utilized that much except for replace by fee, which isn't utilized that much.
Zero two is the number of outputs.
In this case, we have two outputs.
The green parts are the output amounts.
Yeah, and it's eight bytes.
So many of you may know there's 100 million Satoshi per Bitcoin.
Well, you need a lot of space to represent numbers kind of that big.
Let's see, the orange part is the script pub key.
Again, think of this as putting a lock around that particular Bitcoin that only someone with a private key can open.
And lock time, In this case, it's less than 500 million, so it's a block number.
And unsurprisingly, this transaction got in at that block number.
So here's an example.
We can parse a transaction.
We have to unhexify it to make it sort of binary.
And then we can parse that transaction and see the various parts of the transaction.
So study these two things.
It's in tx.py, not ecc.py, so you go to tx.py in your Jupyter, and you can take a look, right?
There's the various parts that I already explained to you, like, let me make this bigger.
There's version, transaction inputs, transaction outputs, lock time, and sort of indicating whether or not it's for testnet.
You can parse it by reading it and byte streams are very useful for this sort of thing.
And you can serialize it or turn it back into a bunch of bytes.
And you can, you know, there's other stuff, there's other stuff like fee and hash to sign and stuff which we'll get to.
Yeah, but You can also play around in transactions, the Jupyter Notebook, and you can see what the transaction looks like.
It's a version one, it's got at least one input, and you got two outputs and a lock time.
Anyway, I'll come around if you have questions.
And move on to the next thing.
All right, so let's talk about script.
I told you that I would be talking about script, right?
What is script?
Script is a limited programming language, and it's not Turing complete.
You can sort of think of it as a smart contract language for Bitcoin.
And it's a programmable way to assign Bitcoins.
I can programmably assign it.
For the most part, people only use the standard ones, which are called addresses.
They're compressed scripts.
Like they're assigning from one person to another.
So how does script work?
Well, there are two types of items, elements and operations.
Elements are just data, signatures, keys, hashes, whatever.
And operations do something to the elements.
So each element is added to the stack, operations do something to the stack.
And at the end of processing all the items, there must be a single element that's not zero left on the stack to evaluate to true.
That's really all it is.
Some common operations, op do, op hash 160, op check sig, op return, they all do various things and you can read about them.
There's a whole list of different ops.
Anyway, parsing script.
Each byte is interpreted as an integer.
If it's between one and 75 inclusive, the next n bytes are an element.
Otherwise, the byte is an operation based on a lookup table.
All right, so zero zero is not between one and 75, so it corresponds to op zero, which puts zero on top of the stack.
Zero five is between one and 75, So the next five bytes are an element.
48 is 72 in hex.
The next 72 bytes are an element.
76 is outside, it's greater than 75.
And op dupe is an operation.
93, 89, and many, many more.
Okay, you can go look them up.
Anyway, some common elements that you might see are public keys in the SEC format that we talked about, compressed or uncompressed, signatures in the DIR format we talked about, Hash 160, these are like 20 byte things as part of addresses.
And again, addresses are compressed scripts.
So you have something called pay to pubkey, which was used very early on in Bitcoin.
These are the ones that Satoshi used.
Pay to pubkey hash, it got a lot shorter.
Pay to script hash, pay to witness pubkey, pay to witness script hash, these are all sort of existing on the network.
Anyway, here's how you do script validation.
You take the script sig field, which is the thing unlocking it, and you process them.
And you look at the previous script pubkey, and you process those.
And if the result leads a non-zero element, you're done.
So You might be a little confused at this point.
That's okay, because I have a nice visualization to help you understand it.
Here is the very first script, pay to pubkey.
And it looks something like this.
It's, you know, here's the script pubkey or the encumbrance.
It's in sec format and you have the pubkey in sec format and then ac which corresponds to op check sig.
And script sig is a spending thing and it has just one element, a signature in their format.
And you can kind of see why it's called script pubkey and script sig, because script pubkey literally has the pubkey in it.
And the script sig literally has the signature in it.
And they're both part of the script language, right?
Like that's why the fields are called what they are.
You'll see later that those don't quite apply anymore.
But here's what you do.
You take the script pubkey, which has those, you have the pubkey element and object sig, and you have the script sig, which has a signature, and you combine them to get these three things.
And you take those three things and you process them one at a time.
A signature is just an element, so it goes on top of the stack.
And then pubkey is also an element, so it goes on top of the stack again.
And then OPCHECKSIG is an operation, so you process the operation.
An OPCHECKSIG checks if the signature is valid for the current transaction, puts one back if valid, zero otherwise.
Well, takes the top two things, looks at it, pubkey signature, say it's valid.
You get a one.
And there's no more elements, so there's one, there's something on top of the stack, it's a one, it evaluates the true, the transaction is valid.
Now it turns out that there's some problems with pay to pubkey, namely that the pubkey is like really big, right?
Like it's a 65 byte thing that you have to pass around for someone to pay you.
And it's also a little bit less secure.
So what they decided to do was do pubkey pay to pubkey.
These are the addresses starting with a one.
I already showed you how to make them.
And they're shorter due to the use of RipeMD 160, which compresses to 160 bits.
And it's more secure due to utilizing elliptic curve discrete log.
You have to break both elliptic curve discrete log and you have to get pre-images of two different hashes.
So you've got like sort of three layers of protection as long as you're not reusing addresses, right?
Anyway, here's what it looks like.
Pay to pubkey hash, you have op dupe, op hash 160, some length of a hash, op equal verify, op check sig.
So this is the script pubkey or the encumbrance, and here's the script SIG, which has signature and pubkey.
So if you notice, pay to pubkey, you move sort of the pubkey from script pubkey to script SIG, right?
Like as part of unlocking it, you reveal your pubkey.
Okay?
And so here's what the combination looks like.
You have the script pubkey, which has opdup, ophash 160, hash, op equal, verify, op checksig.
And then you have the script sig, which has a signature and pubkey.
Great, you combine them and you get this nice stack.
And we're gonna go through them one at a time again.
Signature goes on the stack.
It's just an element.
Same for pubkey.
Now we start processing.
Op do duplicates the top element and puts it on top.
So you duplicate the top element.
What's the top element?
Pubkey, so you duplicate the pubkey.
All right, op hash 160 does a shot 256 then a ripe md 160 to the top element.
Okay, we do that to the pubkey up there and it becomes some sort of a hash.
We put the hash up there because that's just an element.
Op equal verify, checks that the top two elements are equal, if not, fails the whole script, otherwise it gets rid of them.
So Assuming that they're equal, it just gets rid of them.
Otherwise it would have stopped.
And then op checks the signature, takes the top two, checks that the signature is valid with that pubkey, and it is done.
This ends up being a lot shorter, right?
Like it's a 20 byte, you only need to send those 20 bytes in the RIPEMD 160 hash instead of 65 bytes that Satoshi was sending before.
And it's also more secure and things like that.
So I would have you take a look at this, but I think you guys are getting hungry, so I'm gonna kinda go through the next part.
Transaction validation.
So in order to actually validate a transaction, this is what every node in the Bitcoin network does.
First of all, they need to check that the inputs are on spends, right?
Make sure that this is not an attempt at a double spend.
And that's fairly easy to do as long as you have the entire blockchain.
And then you need to check that the input amounts and the output amounts, that the input amounts are greater than or equal to the output amounts.
The difference, by the way, is the minor fee.
So the minor fee is not specified anywhere.
You actually have to calculate it by summing up the inputs and summing up the outputs and finding the difference.
In this particular transactions case, it's $40,000 Satoshi that was paid.
Next, you need to check that the script SIGs are actually valid, and the script SIG sort of unlocks it, and in this case, it has the pub key and the signature, and you need to make sure that the signature is valid.
The thing that you need to know is what the heck is that signature signing?
You need to find the hash of something, but you need to figure that out.
And this is one of the shortcomings of how Satoshi did it, was that it requires a different thing to hash every time for every different input.
And that leads to the quadratic hashing problem which SegWit solves.
Anyway, to check the SIG, we have to empty out the script sig.
Then we substitute it with the script pub key of the output.
So the previous output that you're spending, you put the script pub key in.
And then you append something called the sig hash.
And in this case, we're using sig hash all.
It's almost always sig hash all, and that means the entire transaction goes through or else the signature is not valid.
You could do SIGHASH single, which says, okay this particular output also has to be in the transaction but the rest of it I don't care.
There's also something called SIGHASH none, which says you can spend it however you want, which is like a great way to get your funds just stolen by the miner.
So those aren't really used.
But this is what happens.
You put in SIGHASH all at the end.
Just one note here, Bitcoin Cash uses SIGHASH fork ID and those four bytes at the end somewhere.
There's a bit in there that's for their chain and that's why they're strongly replay protected because signatures for one are not valid on the other and vice versa.
Anyway, we double shot 256 this whole thing to get the thing that's being signed, that's the hash Z.
Okay, and you do the exact same thing that we talked about with signing and verification, you can get the RNS from the DIR signature that's in there, and using that, and the pubkey, using those we can parse and verify each input.
You can take the pub key, you can take the RNS from the signature, and you have the hash that you're signing, and you utilize all of those to see if the transaction input was valid.
So that's the pub key in SEC format, this is compressed, That's the signature from the script sig.
And this is how you would verify each input.
In this case, there's only one input, so it's relatively easy and fast to verify.
But because of quadratic hashing, if you have a lot of inputs, it goes up as the square of the number of inputs.
So there was one block mined by F2Pool a few years ago.
Some guy used the brain wallet cat to send out lots of little outputs They thought they were doing a good thing by combining that all of those UTXOs into a single one but there was a transaction that had five thousand inputs and that took way that took way longer for people to verify because it goes up quadratically.
So it took like a minute to verify for a lot of nodes and that's a lot of time that they're not mining.
Anyway, I would have you study this, but again, I think you guys want to go to lunch, so I am going to leave it to you guys to go study it during lunch or after lunch or tonight or whenever it is you get a chance to read this stuff.
I do want to get this paid a script hash, because this is a really cool innovation that happened, kind of related to SegWit a little bit.
But basically, here's sort of the history behind it.
There was something called Bare MultiSig.
And Bare MultiSig is basically a way of encumbering coins to more than one private key.
So think about a lockbox with multiple keys that are required in order to open it.
Anyway, this was how Satoshi sort of implemented it.
And this is what the script pubkey looks like.
You have a couple of pubkeys.
And you have, this one is a one of two.
The 51 there is op one.
So one of two op check multi-sig.
And the script sig has to look like this.
Op zero, we'll get to that in a minute, and then signature.
And here's the script pubkey, here's the script sig.
You combine them and you get the script, right?
And we're supposed to utilize these, we're supposed to go through them one by one.
The X can be anything, in our case it's zero.
And then we put on all the signatures, you put an M, and then all the pubkeys and N.
This is M of N multisig, okay?
Or five of seven, one of two, three of nine, whatever.
And then OPCHEC multi-sig is, sort of does all the heavy lifting.
It checks if M of these signatures are valid for this transaction.
And puts a one back if that was zero otherwise, so you just sort of end up with a one, assuming M of those are valid.
Anyway, X can be anything.
It's a bug that Satoshi had in the original implementation.
Check multisig consumes one more than is necessary.
So it's an off by one error, and it would require a hard fork to fix, so you just have to put something there.
It consumes one more than is required.
There's no way to really make this an address, right?
It's just way too long of a script pub key.
So people, and big transaction output for the UTXO set, There's a lot of problems with bare multisig.
And this was abused.
This was abused pretty badly.
This is a Stack Exchange question that I answered a few years ago.
But basically, the entire Satoshi white paper is encoded into the blockchain.
If you run this particular script that I wrote as an answer to this question, and you have the entire Bitcoin blockchain, you will get the PDF of the white paper.
It's encoded into the bear multisig, And it's done by putting it into the pubkey, and you just, it's essentially encoded like 64 bytes at a time.
And you combine, it has 937 output, or 47 outputs, and it's 64 bytes on a 2 of 3 multi-sig or something like that and or 1 of 3 multi-sig so there's a there's like 64 times 3 or 192 bytes per output something like that that times 947 that's that's the the size of the entire PDF.
Yeah.
Can you post that on the Slack page?
Yeah, I'll put this on.
Yeah, but yeah, you can literally run a script if you run a Bitcoin full node, and you have txindex enabled, I think.
But you press enter on that script and it will produce bitcoin.pdf and you double click it and it's literally the pdf of the white paper which is kind of crazy.
But that's kind of abuse right?
Like You're sort of utilizing the blockchain for storage and everyone else has to pay the cost of storing it.
Anyway, P2SH was meant to solve a lot of these problems.
These are addresses that start with a three.
You guys might know them.
They're really flexible because part of the script is sort of kept by the creator of the address.
And it's important that as the creator of the address that you keep this, otherwise you can't redeem it.
And that's why it's called the redeem script.
Redeem script must be provided when spending.
Remember how sort of the pub key went from the script pub key to the script sig?
We're doing that for more of the script with redeem script.
Redeem script is at first treated as an element, but then it is interpreted as a script later.
So here's what the script pubkey looks like, A9, 1.4, 7.4, et cetera.
A9 is just op-hash 160, and then you have a 20 byte element, and then op-equal.
And the P2SH script sig is, you have a bunch of signatures, then you have a redeem script.
So here's what it looks like.
You have the script pubkey, op-wash 160, hash, op-equal, script sig is op-0, signature-1, signature-2, redeem script.
You combine them, you get that thing, and let's process them one at a time.
Op zero just puts a zero on the stack.
The signatures and redeem script are elements, so they just go on top.
Op hash 160 hashes redeem script, so it becomes a hash of the redeem script.
Then you put the hash on top and you look at op equal.
Checks that the top two elements are equal.
If so, put a one on the stack.
If not, put a zero on the stack.
So you get a one.
Now, if you are a non-upgraded node pre-BIP16, this is where you stop, right?
And you look at the top element, it's a one, it's valid, and you're allowed to spend it.
But, if you're post-bip 16, you have this special rule.
And the special rule is, if op-hash 160, hash and op equal in that particular order happen, then whatever the redeem script was, you put back on the processing queue.
This sounds like a hack, it is.
It was a hack.
And there's a very particular reason why they made it this way.
And SegWit operates in many of the same ways that this did.
But they did this for a reason.
And this was part of BIP16 and it was hugely controversial.
But anyway, let's look at the redeem script.
Here's the redeem script.
It has two pubkeys, two of two check multisig.
So you take that, you interpret the redeem script as elements of the script and you put it on the stack to process.
So now you go, okay, all right, here's op two, that ends up being a two, and those two go on, and then you do op check multisig again.
It's two of two multisig if the signatures are valid, and of course you guys remember op check multisig has an off by one error, so it needs a zero at the bottom.
But anyway, if it checks out, then you get a one and you're done.
So upgraded nodes do this checking, this special checking at post-BIP16.
But pre-BIP16, they just go up to right before the special rule and they sort of terminate at that point.
But that was sort of a big innovation.
And it was made new as part of the introduction of P2SH and BIP16.
Redeem script will be added to the processing queue only if the hash matches the hash in script pubkey.
And redeemed script substitution is a bit hacky.
It was a huge controversy.
And I think it passed with 55% or something like that.
And it was sort of a segway of four or five years ago or something like that.
You said it's controversial.
Uh-huh.
If you pass by 55% of what group, who's discussing this in the session?
Well, so it's a soft fork.
So you only needed, like, it was possible to spend the redeem script without actually having valid signatures and stuff like that.
It turned out that a majority of the mining hash power went with BIP 16, so the minority fork never, like was always overtaken, so nobody really tried to do that.
And that's how it was enough to, you know, I think it required like a new version number in the block, which was two or something like that at the time.
And that's how they signaled it at the time instead of bit nine, which we do now.
Anyway, here's what a pay-to-script hash transaction looks like.
Again, version, inputs, previous transaction hash, previous index, and you can see this giant script sig.
Most of the time the script sig's gonna be the largest part of a transaction, and it is certainly here.
Sequence, number of outputs, there are four outputs, and you can see that the orange ones are the script pubkey, pay to pubkey hash, or addresses that start with a one.
That red one is a pay to script hash, but a script pubkey, and it looks a little different the orange one start with 1976 a 9 1 4 Though the red one starts with 17 a 9 1 4 so they're they're slightly different.
It's 2 bytes shorter and Yeah, you can sort of identify it after a while if you've been working with hex transactions.
And then you have lock time.
Anyway, you create a P2SH address very similarly to creating a normal Bitcoin pay-to-pubkey hash address.
Bit 13 defines exactly how you do that.
For main net, you prepend byte five.
For test net, prepend byte C zero.
And you can use the functions there and you can check it out.
Do I have more stuff?
Yes, I do.
All right, all right.
So I'm going to skip that so I can get to actually verifying this, the pay to script hash transaction.
So you have signatures in the script sig.
And what did this sign, and how do we verify it?
And this is something that everybody needs to do, or every node needs to do in order to validate this transaction.
Well it turns out we have to do something very similar as before, we replace the script sig with zero, but we have to put in the redeem script instead of the previous script pubkey.
And I have to tell you this information is not around in many places.
I searched for three days back when I was trying to learn how to do this, and I finally found out this is what you had to do is to put in the actual redeem script into the script sig field, and then you add the sig hash as before, and then you hash this thing, and that's what gets signed.
And Once you have that thing, then you can take the pubkey and get the RNS from the signature.
Since it's in DIR format, that's what it looks like and this is how you parse it.
And you take the pubkey from the re-theme script And then we can verify using the pubkey and the signature and the hash of the thing that we figured out how to get.
But anyway, yeah, it's like 1147.
So I will, yeah, I think, Are we late for lunch already?
Or can we go a few more minutes, Anton?
Okay, all right.
So why don't you guys study all of this stuff.
Like I skipped over a bunch of them, but try them out.
I'll show you what they look like here.
Here's transaction verification.
You can see that it returns true.
Here's how you do P2SH addresses.
Here's how you do P2SH verification.
And you can take a look at TX.PY.
And just sort of study it on your own time or whatever.
There's a lot of functions in here that might be interesting or useful.
You can figure out what hash to sign.
This is always a giant pain because of the bad design around the signing, which SegWit thankfully fixes a lot of.
And then verifying inputs, signing inputs, things like that, you can take a look at it.
Ask me any questions you have, I'll be walking around.
All right, so I think there's plenty of you, for you guys to study and stuff.
Are there any questions regarding any of what I've covered so far today?
Yeah.
Realistically, what does it look like as far as like a heart limit on how many people can participate in the whole institute?
Well, I think limit is 15.
Yeah, I think and that's there's some hard coded thing or some limitation.
I forget exactly which one.
Any other questions?
You guys are all hungry, aren't you?
All right, I think Anton will lead you to lunch.
Follow this guy.
I can turn this off.
All right, I think we're good.
Thank you.
Thank you.
Thank you.
You you

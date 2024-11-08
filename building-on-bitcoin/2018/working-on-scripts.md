---
title: Working on Scripts with logical opcodes
transcript_by: Bryan Bishop
tags:
  - scripts-addresses
speakers:
  - Thomas Kerin
date: 2018-07-03
media: https://www.youtube.com/watch?v=A4l4waikDso
---
<https://twitter.com/kanzure/status/1014167120417091584>

Bitcoin has logical opcodes in bitcoin script. Depending on whose is trying to spend coins or what information they have, they interact with logical opcodes. We could see a simple example here taken from one of the lightning network commitment transcraction scripts. It pushes a key on to the stack so that a checksig can run later. It adds a relative timelock as well. Two people can interact with that script and we can set different constraints on those.

IF you're trying to write software that will sign and interact with these, it can be some pain to sit there and work through them case-by-case to how to interpret them and process signatures. When there's multiple branches in the script, the requirements idffer from branch to branch. So there needs to be software methods for smoothing scripts into separate branches.

Logical opcodes control the scripts execution flow by managing a stack of booleans in vfExec. Before every opcode is interpreted, we check if execution is currently active. This is fExec check, otherwise nothing happens.

OP\_IF pushes the fValue directly. IF and NOTIF pop from the mainstack and cast the value into a boolean. This changes flow control. They work by converting whatever stack value they found into a boolean and doing something with it, in the case of NOTIF, and pushing it on to the stack. This interacts with fExec checking if execution is active. These opcodes are what we use for testing conditions.

There's ELSE and ENDIF where ELSE just modifies the firsy value on vfExec to modify execution, if it wasn't executing then ELSE makes that value true again. ELSEIF will pull you out of the conditional section and removes values from the vfExec.

Traditional scripts don't make use of this. fExec is always true. They are pretty easy to analyze and work out what's happening. It's pretty easy to reason about what steps you have to do to actually sign them. With pubkeyhash requirement, you can produce a signature and figure out how to sign that transaction.

Here's an example from bip114, it's a hashed timelock contract. Iam using T to signifiy that fExec is true. There are three branches, and under each one, there's a t for whether it was executed or not actually executed. Under the pathways, different paths are active. .... in some situations, different things are required in terms of their input. And what signatures would be required to satisfy what was necessary?

Just to point out something, the values that both each of the paths there, the 0s and 1s, those are values whatever would have been pushed by IF and NOTIF.... and led to this codepath... These are the values that IF and NOTIF would push into the fExec stack to cause flow control to go in different directions. They are unique and they all uniquely identify a different branch. If they are executing, there wont be false values in the stack. If you want to go into the second branch, then that first IF would push a false value... so that's what.. the 0s and 1s are doing there.

To identify contents of branches, and suppose that we have software that can sign any script including these kinds, we probably need to be able to identify the branch so that they can take the branch in isolation and see what the requirements are. We can iterate over the script instructions and partially interpret them- we only need to look at logical opcodes and track some state about them. Whenever we encounter an IF or NOTIF, we know we have a separate code block or conditional to consider. Each one means we have new code paths. And opcodes may or may not be associated with that.

We just proceed over the whole script, we associate all the opcodes with each codepath.... So since this is a general method as well, we want to check for valid or invalid scripts. If any codepath while we're tracking the changes to the vfExec.. if by the end of the script, it's obviously invalid, it wasn't fully balance,d, so we can reject those. I have really... nasty slide, ... just what it's doing there, and yeah, at what point information is known.

You can see here there's a box without anything in it. This represents no execution yet. Then we run into the IF, and then there's a conditional section, and it would have to be true to enter that part, and there's no further nesting in that branch where it was one.. so it oesn't go any further. We then see that the ELSE opcode indicates it could have been 0 or false... we also see there are further conditionals... and they are the same values we wound up for naming... our code paths earlier...

I wanted to look at mutually-exclusive opcodes in different branches of scripts.

I also wanted to see about converting standard scripts into MAST bip112 versions or even bip116+bip11 with tail call semantics.

In the flattened script, in the example I show here, the DUP opcode is completely eliminated from the script. You can also look at-- stack instructions only relevant in certain branches. You can look and see that a DUP is removed so you can remove one of the DROPs.... In the last one, there's no sign of hashlocks even though those were the cases where Bob didn't know the first hashlock or not... and so you have to go look at whether the hash was required in the outcome of the script. Generally that was the problem I wanted to tackle and found really interesting.

MAST isn't on the network yet, but I still found this interesting ffrom a script library perspective. It woudl be interesting to make sure that you weren't signing the wrong branch or revealing the wrong preimage or whatever.

Trim instructions used by the old script purely for flow control purposes, which are unnecessary in a MASTified branch (hashlocks, for example). Any logical operators, which are just tests for flow control stuff, can be replaced with flowcontrol assertions of values on the stack. So you could use verification opcodes instead. Also, you can further tweak things by you might see a CHECKSIG which is now VERIFY now. Those can be merged together and you are less likely to run into the opcode limit.

<https://github.com/kallewoof/btcdeb>

<https://github.com/Bit-Wasp/bitcoin-php> (has branch parsing but not MAST)

There's also a web tool by Nicolas Dorier for MAST stuff, including branch parsing but without instruction optimization. He has someone for MASTifying.. has similar issues... doesn't remove unnecessary instructions.

Q: How do you run these scripts?

A: btcdeb, bitcoin-php, or even libbitcoin's consensus library.

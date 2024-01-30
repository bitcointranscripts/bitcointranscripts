---
title: "Default Fee Rates and Wallet Privacy"
transcript_by: zachbitcoin via review.btctranscripts.com
media: https://www.youtube.com/watch?v=R1rmT7ue1HA
tags: ["wallet","privacy","fees"]
speakers: ["Randy Naar"]
categories: ["conference"]
date: 2023-02-16
---

**1. Introduction and Overview**

"I'm going to make sure I can get all the threads in. Yeah, perfect. Oh, this is not working. All right, so my talk is on fee rates and wallet privacy. My name is Randy. I'm a software engineer at Blockstream. I typically work in applications for Liquid, but today I'll be talking about Bitcoin and how you might reduce your wallet privacy by using the default fee rates of your wallet."

**2. Understanding Transaction Fees**

"Before I get started, I wanted to go over some context about these fee rates. So a couple questions. What are transaction fees? Size versus virtual size, and why are fees important? So what are transaction fees? Transaction fees, they're the difference between a Bitcoin's transactions inputs and outputs, if you didn't know that. And the fee is pretty much equal to the total input amount minus the total output amount. Yeah, I know it shows up kind of small and that might be a problem for later slides. I hope it's still okay right now. Fees, they're implicit in a Bitcoin transaction and can be set to any arbitrary amount, assuming you have the funds to pay for it."

**3. Wallet Fingerprinting**

"So what I'm actually gonna get into today is wallet fingerprinting. If you're not into web dev and things like that, there's server fingerprinting, which is like figuring out what server software a specific web server is using. And Here, the concept is very similar. It's trying to figure out what wallet implementation a user's using based off their transactions. So hence, wallet fingerprinting. I actually had some inspiration for this. If you guys know, Andrew Chow, he had a talk, I guess, at Bitcoin hackathon that I went to, it's the previous Bitcoin++ and he kind of, this is the QR code for that link to the YouTube video and he also has a repo on github."

**4. Default Fee Rate Variations**

"The question that I have to answer before I can see whether I can identify someone's wallet, depending on their transactions, is can wallets vary in the default fee amount? And the answer is yes. So for the same transaction, you can have varying transaction fee amounts, depending on the wallet that you're using. So why are the fee rates different? Naively, you might assume, well, they're using different fee sources. And they do. Blue uses Electrum. Green uses the Green Server. Wasabi uses blockchain by default."

**5. Technical Analysis and Experiments**

"So there's a fee algorithm for Blue. And Here, I can read what I wrote here. The bluewallet uses a fee algorithm that multiplies the fee rate for each category of fee rate, so fast, medium, and slow, with the fee rate calculated from one block of mempool, and divides it by the fee rate for one block calculated by Electrum. And that's like a lot of jargon I'm gonna show you, a code snippet that hopefully you can see a little bit from that."

**6. Wallet Tells and Privacy Implications**

"So as you see, it's kind of hard to read through. But yeah, the basics of what Wasabi is doing is they have this interpolation for the feed algorithm. And again, I- how do they do? Recommend, or if you want to get any of these links afterwards as well, you can flag me down and like, you know, I'll be happy to. So if- if they're interpolating, for example, they- they- they get numbers of 3, 5, 10 and they interpolate 7, let's say. Right."

**7. Discussion and Q&A**

"Does it make sense to, for example, try to be like Bitcoin Core or be like Electrum, for example? Yeah, we were having some discussions where you could either hide in plain sight, right, where you could try and share a fee rate with whatever is the most popular being used, Or you could have some kind of variance. You could put some randomization in it."

**8. Conclusion**

"The talk's pretty much over. The conclusion is, wall-fingerprinting can definitely be a threat to your on-chain privacy via the analysis of fee rates, but whether that trade-off of privacy for convenience is worth it, up to you. That's pretty much what I can say. Some users may not care about this, but I think at the very least everyone should be aware that this is a leakage of information. And yeah, so thank you. That's all I have for this talk."

(Applause)



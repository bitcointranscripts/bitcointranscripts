---
title: Lightning Payments
transcript_by: Bryan Bishop
tags:
  - lightning
speakers:
  - Will O'Beirne
date: 2019-05-11
media: https://youtu.be/wd-dNd2Wck4
---
Lightning payments (and more) on the web

CL: Thank you Elizabeth and Stacy for that great talk. Who runs a lightning node here? So a lot of you. Are you guys excited about lightning? Great, we have like four more talks on lightning. Next we have Will O'Beirne who will be talking about lightning payments on the web. Big round of applause.

# Introduction

Hey y'all. We're doing a DIY setup here. Just bare with me. Alright. It was great to hear from Elizabeth Stark. Today I am going to be covering a less technical more user experience thing, actually using lightning on the web for payments and a few other things. I'm going to talk about bitcoin payments and where we are going next.

# Background

I work on a browser extension called Joule. It plugs into the browser and makes the lightning experience on the web better. Before that, we have to talk about bitcoin payments.

# Bitcoin payments on the web

Bitcoin was envisioned as a p2p cash system but there's some problems. You need to send an address, but it might be the wrong address, and you might send the same payment twice. Depending on who you sent it to, they might not want to fix your problem. You also have to deal with long confirmation times, and there's explicit expirations on those payments. If you set a low fee or the mempool is too bloated, then the transaction might not go through. There are also high fees making small-mid size purchases infeasible. So this means small prices aren't a good use case for bitcoin payments. Also, you either need a new address with new UTXOs for every address, or you had to set the same address, which degrades privacy.

# Lightning webapps

Thankfully lightning improves a lot of these problems. What do lightning payments on the web look like? Payments are done through invoices. The server provides an invoice and the user pays to that specific invoice. They have a set amount, an expiration date for the payment, and where it's going, and it only works once. You will always send to the right person within the right time limit and never spend twice. Once the payment goes through, it goes through instantly, right away.

Unfortunately lightning payments do come with problems, like sometimes you can have routing issues where you can't find a route to your server and the server won' tknow that you are experiencing that problem. They have no idea what's going on, it's totally opaque. So you would have to switch to another mobile app if that's the case. It's still high friction.

# High friction

High friction is bad. When you have to stop a user, it's bad UX. Users might bounce from lightning micropayments on a website. Bulk-purfchasing tokens or long-term subscriptions are also bad. You want to pay only for the content you want. This is a good practice. Sometimes the tokens don't work because you won't be getting your money back anyway if you don't spend them all.

# Custodial nodes

Another trend in lightning is custodial nodes. The payment process is annoying, and you deposit to a central node. So you make one payment upfront, then they control that database and when you want to withdraw the money, you give it an invoice and then they do the payout. None of this is on the network which is fine, but you're locking up your liquidity on these sites for every site you have deposits at. So this is problematic. Also, it doesn't take advantage of the network effects of the lightning network. It's still a hub-and-spoke model of paying central services.

# Purchase permanence

There's this variable purchase permanence.... say you need to have a login like a username and password to login to some service. But many purchases are so small that they are just tied to the device. Here's something about yalls.org and you bought an article on the desktop. It's a small payment, it's not that frustrating, but there's these things we have paid for but can't get access to again. Sometimes these payments are ephemeral and small and so meaningless that once you close the tab maybe you don't care anymore.

# Summary

There's a lot of improvements over bitcoin payments, but compared to paypal, a lot of the problems are still there. There's a lot of friction in these. Payments between users are still managed centrally, and micropayments are still not viable user experiences. Also, you still need traditional authorizaiton on websites.

So we have ended up with something better than bitcoin payments. But it's hard to see why you would use this over paypal or something.

# WebLN

I am working on WebLN to make this better. It's a standard for providing permissioned access to community web applications and your lightning node. The idea is that the user client injects an API into javascript, and the website can ask for user permission to do more direct payments. We're improving the user expeirence and getting rid of the friction, but we're still preserving privacy because the user still has to give permission. It's not a direct connection to your node, it runs through your browser which keeps some privacy in-tact.

# In-app interactions

API interface allows for node interactions entirely in-app. It's a much more instantaneous experience. No alt-tabbing or copy-paste. If something goes wrong with your payment, then the application-- like a routin failure or someone has a low balance or something or some connectivity issue-- the application can assist in fixing what's going on. And you have just lowered the friction of these payments, so it's not so bad.

# p2p

There's also enabling the p2p use case. There's a lot of ways to facilitate p2p payments. We automate invoice generation, we just pass the invoices to the server, and we just facilitate payments between users. It's either in your node or in the node of the person you're paying. This is a much more decentralized attitude and leverages the network we're building.

# Identity and proofs

You can use your node identity to establish who you are in the network. The user can opt-in to provide their LN node identity and then prove that identity with signatures. You can also provide old payment preimages as proofs to recover past purchases. They don't have to recognize who you are, only that a previous payment was valid. You could have users authenticate with a node, instead of paying for that website or some pseudo-unique identity like email/password then you can just check are they a good member on the network because they already have an identity for their LN node. Or maybe you give them a discount because they are helping out on LN liquidity.

# Confirm-free experience for payments

In previous UX, there's a popup to confirm. But this here, the idea is to not ask the user if the amount is below the threshold. The app could potentially request information before a high usage activity. But otherwise, it pays automatically. So the user can setup the allownace beforehand. This gives us a true micropayment experience that wasn't previously possible becaus ethe user experience was so bad.

# Programmability

Nodes have APIs and they are on 24/7. We can use that power to have the node talk to the server and not have a user involved. I launched Tippa yesterday. You upload some authorization to your node, and then whenever someone wants to make a tip, the server doesn't hold on to it for you. It's similar to cookies, it's a fancy cookie really. I can give permissioned access, like you can only generate invoices and not identify who I am. So there's a lot of endless possibilities using this.

# Client and node agnostic

All of these features are client and node agnostic. The user client now comes with this stuff. It is tailored for better experiences. There's the Joule extension and the BlueWallet phone application. This stack can be used with any LN node, I'm currently using lnd but that's not a requirement. Also, more people are building on top of this today.

Hopefully we end up with happy users who are having good experiences on the web and they will make a lot of payments on the web.





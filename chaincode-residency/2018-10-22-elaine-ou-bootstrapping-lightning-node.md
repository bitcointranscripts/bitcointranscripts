---
title: Bootstrapping and Maintaining a Lightning Node
transcript_by: Michael Folkson
tags:
  - lightning
  - routing
speakers:
  - Elaine Ou
date: 2018-10-22
media: https://www.youtube.com/watch?v=qX4Z3JY1094
aliases:
  - /chaincode-labs/chaincode-residency/2018-10-22-elaine-ou-bootstrapping-lightning-node/
---
Slides: https://lightningresidency.com/assets/presentations/Ou_Bootstrapping_and_Maintaining_a_Lightning_Node.pdf

# Intro

My name ie Elaine. I’ll talk about bootstrapping and maintaining a lightning node. Pretty much all of you have probably already set up a node so this should all be review. You guys will probably know more about this than I do.

# Bootstrapping and Maintaining a Lightning Node

We’ll start with an overview of how routing works just to understand what the nodes are trying to do and from there we’ll step back and look at ways of finding peers and getting incoming channels and maintaining capacity.

# Calculating a Route

We’ll start out with route formation, in theory. When you want to make a payment you have to figure out how to get it there yourself even if you’re not directly connected to the recipient. In the Lightning Network, routing is source-based which means it’s up to the sender to figure out a working route. The way of finding a route varies by implementation. Routing isn’t specified so it’s still open-ended and by no means a solved problem. The Lightning Network itself uses onion routing. Intermediate nodes only know who they should forward each packet to. They know about their predecessor and their successor but they don’t know the packet’s origin or the final destination. The nodes along the way can’t help you out midstream. This makes routing more flexible and keeps transactions private and gives participants anonymity. Every node in the network has their local network view and from there they have to figure out some number of best paths to try. The criteria that’s taken into account by a payment ended is determined by the transaction fees, the payment fees along the way. Also they take into account the timelock that will be incurred. Right now, every node that helps to forward a payment from the sender to the recipient accepts the risk that the timelock payment will timeout before the timelock payments gets fulfilled at the endpoint. Because of that, every intermediate node will add some timelock delta to the next timelock payment that it forwards. When a sender is determining the best route to take they’ll take into account both the timelock penalty because they don’t want to have a potential really long timeout wait period and also the fees because no one wants to pay fees.

Q - Isn’t there another consideration for having a longer path for privacy reasons - not including certain intermediaries?

A - Absolutely. Right now it’s a simplistic view and it’s how the implementations do it right now but there are certainly better ways of doing it. For now, the sender will basically do a best first search to find some number of paths to try. lnd uses Dijkstra’s algorithm and I think c-lightning uses Bellman-Ford which is similar but can also take negative fees into account because sometimes nodes will have a negative fee on their channel if they want to encourage more payments to get routed that way.

Ok, so let’s say Node C wants to send something to Node H and it comes up with three different paths of increasing cost according to their cost function which takes into account the fees and the timelock penalty. The different Lightning implementations are getting more consistent with error reporting so maybe C tries the first route and discovers that the channel from F to H doesn’t have sufficient balance to forward the payment. So then it knows to skip the next path and then go straight to C - E - G - H. Ideally we have at least one path that works and the payment goes through.

# Routing (in practice)

In theory it works but in practice we often get a lot of errors. Sometimes the payment failure feedback isn’t really good and then people complain and concern trolls will say Lightning doesn’t work and routing won’t work. Our goal here is to make it so that this happens as infrequently as possible.

# BOLT 10 - DNS Bootstrap and Assisted Node Location

Based on that we have to figure out how to make friends. Choosing which nodes to form channels with will help us prevent that from happening. When a node first spins up a Lightning instance it doesn’t have any peers yet. You need peers to get started and find out information about what the rest of the network looks like. There’s currently a DNS seed server that indexes nodes and pulls out a random set of nodes for bootstrapping. This is similar to the one that is used in Bitcoin. I think only lnd uses the seed server right now. It is also useful because if a node doesn’t have a static IP address it can go offline and come back. This is a way to find the node again if its IP address has changed.

# BOLT 2 - Peer Protocol for Channel Management

Presumably a node can contact the seed server, find out about what other nodes are currently in the network, then it has to open channels. I won’t go too much into the details of how channel formation works, I think Chris did a good job of providing an overview of that. Basically a channel is opened when the person funding the channel, in this case Node A, sends an open_channel request to Node B. The open_channel request has a bunch of fields in it like the funding amount, the push amount which is the initial amount that goes to Node B and other stuff like the channel reserve, the delay to wait for a timelocked payment. For the most part Node B can either accept the channel or reject it. For the most part there isn’t going to be a lot of complaint from Node B if Node A wants to create a channel. In the early days there was some difficulty in creating channels because there were different thresholds for what different Lightning implementations would accept for channel openings. Right now, most people just use the default settings and that makes interoperability much easier. Let’s assume Node B responds and accepts the channel opening. There’s going to be a revocation basepoint from which we can derive leverage to punish misbehaving nodes in this channel. Node B accepts the channel. If you think of a channel like a smart contract then opening the channel is like the offer and then if Node B accepts they’re basically in a contract together. They agree they’re going to operate this channel. Node A will create the funding transaction onchain and the funding is then locked, they both acknowledge it. Now they can use the channel.

Q - Are funding_created and funding_locked absolutely necessary enough to go on the blockchain?

A - The funding isn’t actually broadcast when the transaction is created.

We’ll pretend that this is just a private channel between A and B. It’s not forwarding payments for anyone else. Node A sends some update messages to add more timelock transactions and they can commit the transactions with a signed commitment. Node B will reply with a commitment preimage for the previous commitment. Node B will revoke and acknowledge each new commitment. Basically every time a commitment is created there’s a public key that’s created that is associated with the commitment. If the commitment later becomes revoked because a newer commitment is created then the person who has the private key for the revocation can claim the amount in the channel. The revocation key is created using the previous commitment and the revocation basepoint. If Node A tries to broadcast an older commitment then Node B can see that and derive the private key because it had the revocation secret and claim all the money for itself. On the other hand Node A would have to wait for the delay that they initially agreed upon when creating the channel to try to spend the money. This gives B some time to react. It also creates the encumbrance that Node A could have their money locked up if B disappears. If Node B disappears that becomes a liability for Node A because they probably opened up the channel with the intention of using it to make payments or using Node B as a routing point to send payments elsewhere. So an unresponsive Node B means that now this channel is stuck in limbo for some amount of time. It’s kind of a pain in the butt for Node A. We want to be able to create channels and not run the risk that our counterparty in the channel disappears or misbehaves.

# Finding Good Peers

One of the most critical things in finding a good counterparty to open a channel with is that they are going to be online. A node that goes offline renders the channel not very usable. Aside from that, we also want nodes that will maximize connectivity to the network. Every time a channel is opened that’s some amount of money that is locked up. We don’t want to have to create lots and lots of channels to everyone we might want to pay. If we can create just one big fat channel to a node that already has high connectivity that’s more useful than a channel to an isolated node. There are directories, 1ml.com is a pretty good one, where you can see which nodes have a lot of channels connected to them. You can sort them by how recently they got new channels.

Q - If you open a channel with one of these nodes are you the only one providing funds to that channel or do they provide some funds…?

A - The node who opens the channel is the one who puts money on the line.

Q - So what would happen if you just wanted to be paid through Lightning, how would you achieve that?

A - You would have to convince someone to open a channel to you. We’ll get to that in a little bit. Basically the funds are going to be tied up so you have to choose wisely.

Q - Let’s say I’m paying…. can they function as routing nodes to me?

A - Sure

Q - What do you mean with balanced channels?

A - Yeah that’s a good point. Ideally you want a channel that can support payments going both ways. Right now, the only information you have when you see a channel is the capacity which is how much it can handle. You don’t know if all the money is on one side of the channel or the other. That’s a still a problem that isn’t solved.

Q - I think it’s design right?

A - It’s design for privacy because if you can see the changing balance on each side of the channel you can see who is paying who and that’s not very good. Nodes are trying to do the best they can with limited information.

# Autopilot (LND)

lnd has a function called Autopilot where it can automatically open channels to different nodes for a new node. Rene I know you’ve written some critiques on Autopilot. Autopilot right now is not recommended for mainnet but it is good to understand what Autopilot is trying to achieve so we know what the goals are in creating new channels. The way Autopilot works is that it opens channels to nodes. The user can specify the maximum number of channels it wants and the fraction of funds to commit. Then Autopilot will select a random set of nodes to connect to. The probability of connecting a node will be weighted proportional to the number of channels a node already has, according to a power law distribution. Nodes that already have a lot of channels have a higher probability of getting more channels opened to them. It’ll ultimately result in a lot of hubs, a lot of nodes with lots of connections. If everyone were to use Autopilot we would end up with a scale-free network. The hub and spoke model has got a bit of a bad reputation because people think it means centralization where they’re critical points of failure. Most social networks tend to be scale-free networks. Nodes will cluster around super connectors and this makes communication more efficient between nodes. As long as there are many super connectors there’s lower risk of a single point of failure. The network is still relatively decentralized even though there are a lot of super connectors.

# Additional Considerations

The autopilot only takes into account the nodes with existing channels. There are a lot of other considerations a node maybe can’t take into account or doesn’t currently take into account but should be a factor when choosing whom to open a channel to. As Rene mentioned, channel balance. Even though a channel might have large capacity, the capacity might be all on one side which means it can only handle payments going in one direction. Reliability and uptime are also currently not recorded so you can’t tell how often a node goes offline. Then there’s also path diversity and redundancy. You don’t want to be wholly dependent on a single node to do your routing for you. You want to make sure that there are alternative routes if one of our channels go down. Also ultimately, choosing a node to open a channel to is going to be an independent, personal decision because most people are going to primarily shop at a few different stores over and over again. They would want as few hops as possible to get to their favorite destinations. All these factors here are optimizing for outgoing transactions or outbound channels that you create yourself. We know how to send money elsewhere but if we’re operating an app or a store we want money to get to us, we want people to create channels to us so that we can receive future money.

# Why would someone open a channel to you?

As we mentioned previously, someone opening a channel to you is a smart contract. It represents a commitment and it means that both parties are going to commit to operating a channel. Creating a channel with a flaky node is going to cause routing failures and payment delays and it’s a bad experience for the funder of the channel. It can be tricky for a new user to convince other people to open channels to them. One solution is to be a good routing node but that’s kind of a chicken and egg problem because in order to be a good routing node you need a lot of incoming channels. You can’t get a lot of incoming channels until you already have a lot of channels. Another strategy is to just build a store that people like and force them to open channels to you in order to pay you. That’s kind of sub-optimal. You can also just pay for the channel yourself since we’re all going to be using Lightning for everything anyway we can just create a channel, put some funds in it and start spending money at other places that take Lightning payments. If we have a funded channel and push some of it out that means we now have incoming capacity. A lot of new users would create channels and then fund the channel and inadvertently push some amount to their counterparty because they didn’t know that’s actually a commitment to spend the money.

# Exchange On-chain Bitcoin for Lightning

The other two options are one, to exchange onchain Bitcoin for Lightning payments. Zigzag.io is an example of such an exchange. They let you buy Bitcoin on the exchange and the exchange then opens a channel to your node and pushes the funds to you. You’re basically paying onchain for offchain or Lightning Bitcoin. You can also do it the other way round.

Q -

A - Ok, cool. If you have questions about it you can ask them.

One benefit of buying Bitcoin from an exchange and getting Lightning in return is that now you’re connected to a hub. If a lot of people do this then you are automatically connected indirectly to a lot of different Lightning users.

# Non-custodial swaps

Trusted third parties are security holes. There are also non-custodial swaps because in the case of Zigzag or an exchange, the exchange is in charge of sending the funds to you and taking your payment. We can also do atomic swaps. You can create an invoice and then create an onchain timelock payment that contains a hash of the invoice preimage. When that invoice gets paid by someone else you’ve basically done an atomic swap. There’s no trusted exchange involved. Alex built submarine swaps which is one way to do it. Sparkswap.com is another exchange that matches up different people who want to perform atomic swaps on different chains. In both cases you still do have a central party but the job of the central party here is to match up buyers and sellers and so create inbound channels so that the payment can be sent through.

# Why Payments Fail

So now we have some ideas about how to get inbound channels. We want to maintain channel liquidity so that payments can be consistently routed to us or through us. There are a number of reasons why a payment might fail. Sometimes you can’t find a route at all because a new user just doesn’t have enough channels to well connected nodes. Sometimes a payment is too large. Right now, the payment size on Lightning is limited on mainnet. Some large transactions right now are better off onchain. As a Lightning node operator, large transactions are not convenient because a large transaction getting pushed through would imbalance the channel. Then there’s also the problem with zombie nodes. As we saw early on, sometimes people make channels and one participant in the channel goes offline and this information isn’t relayed correctly. Payments generally fail if the sender has not enough information.

# BOLT 7 - P2P Node and Channel Discovery

There’s very limited information that gets shared over the Lightning Network through regular gossip. There are channel announcement messages that announce new public channels and then there are updates for fees and timelock expiries. Not all channels are public and there’s basically a flag you can set when creating a channel. Some nodes won’t accept public channels because they can’t commit to operating the channel. Once a channel is public, it means you’re willing to route payments for other people and then anyone can start using your channel. Not all channels need to be public.

# Let Nodes Do Their Jobs

For most users that are simply doing payments or occasionally receiving payments, they don’t need to create public channels. Right now, I think channels are private unless announced. Many users including myself like making public channels because then we can see ourselves on Lightning explorers and other people connect to us. I can show my mom that I’m cool and lots of people want to make channels to me. But then if I disappear because I have a flaky connection then that’s really bad. It’s basically false advertising on my part to make myself public and accept connections and then disappear. I’ll invoke Adam Smith here on the idea of division of labor. Different nodes are going to be better at different things. Not all Lightning users will need to be routing nodes and not all Lightning users will be expected to stay online and maintain channels all the time. Ultimately in the network, there will be probably be a number of nodes that are there just for routing. They’re earning money from fees so they’re incentivized to stay online and maintain balanced channels.

# Routing Hints

As a Lightning user, even if you don’t have public channels you can have private channels and then provide people who want to pay you routing hints in their invoice. When you create an invoice in Lightning you can add a field that indicates what some intermediate nodes are so the payer can find a path to you even if you don’t have any public channels available. This way if more people make their channels private then the information that nodes have will be more reliable.

# Be a Good Node

Ultimately you want to be a good node and if you have public channels, keep them balanced. You can set negative fees to encourage transaction flow across the channel. Also if you’re going to disappear for a while, close the channel with your counterparties instead of leaving them hanging. Also you can be a good node by punishing bad nodes. You can close off channels that have been inactive for a while.

Q - If you’ve got a channel with someone else and they have a lot of funds on their side but not much on your side, is there a way to swap that up without having to completely close the channel?

A - You can use that counterparty node as a route for something else but ultimately if you want money to go the other side you have to spend money on something.

Q - I mean just adding more funds…

A - Like rebalancing? At the moment you would need to close the channel and add more funds but in the future there’s going to be splicing where you can resize open channels. It’s still all work in progress. Right now, high capacity channels are very scarce. Soon there will be multipath transactions where you can split a payment up over many channels to distribute the payment and not be constrained by the maximum channel width.

# Lots More

In the future there will be splicing where you can resize open channels and channel factories where payment channels can be used to create more. We’ll go into details about this but other speakers know more about that than I do.

# More Information, Better Decisions

Ultimately, nodes will start accumulating more information and be able to make better decisions. I think future implementations will allow nodes to track more metrics about past routing successes and failures so they know which channels are duds and which nodes are flaky. Users will also be able to find out more about which channels were closed unilaterally, by just one party because the other one disappeared, or which ones were mutual closes because you can go on a block explorer and look at the closing transaction. If there was a long timelock on the closing transaction then you know it was a unilateral close. Active node management will also help to inform the Lightning developers how to create better strategies for finding paths and choosing nodes to connect to. So just to show how far we’ve come this is what the Lightning Network looked like in January and this is what it looked like a couple of weeks ago. We’ve come a long way and hopefully in the future we’ll see less of this and more of this.

# Q&A

Q - Today if I want to be a good node what tools are at my disposal to know how I’m being a bad node?

A - You can watch your channel to see if people are actually using your channels. If you’re being a good and helpful node you’ll probably see transactions being routed through your node.

Q - When you say watch your channel are you talking about logs, what tools are available?

A - The command line tools will show you what fees you’ve earned from operating your channels so you can know if they’re being used.

Q - How likely is it that nodes will game the system? Is there any way to detect that?

A - Capacity can’t be lied about because you can see the funding transaction so you know exactly what’s locked up. The channel balance? Right now that information isn’t being communicated at all. It’s more of a trial and error thing. You can try to push a payment through a channel and if it doesn’t work you know it can’t handle it.

Q - If you don’t know the channel balances realistically how many times do you have to push a payment before you find one that does have the correct balance to push a payment through. A lot of times you could run into channels that have been exhausted in the direction you’re trying to push a payment.

A - Information is updated in real-time so nodes might have stale information.

Q - Does most node software take account of that internally or is that something you have to explicitly say as a developer, ok that didn’t work let’s not try that node ever again.

A - I think with lnd a node has one chance to do a do over, I’m not 100% sure of that. After that it goes on a blacklist.

Christian - We just temporarily disable a channel for that node and then try another one. We don’t blacklist nodes if its channels are failing.

Q - Is the blacklisting in lnd forever? If a node doesn’t work at some point in time and becomes a zombie node, lnd will blacklist this node and never use it again?

Alex - It’s the path finding algorithm.

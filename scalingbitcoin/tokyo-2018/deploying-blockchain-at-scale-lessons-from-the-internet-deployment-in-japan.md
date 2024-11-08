---
title: 'Deploying Blockchain at Scale: Lessons from the Internet deployment In Japan'
transcript_by: Bryan Bishop
speakers:
  - Jun Muai
---
<https://twitter.com/kanzure/status/1048373339826188288>

Okay. Good morning everybody. Good morning? I am from Keio University. Welcome to Keio University.

Let me introduce something about our university. This is very old. It's from 1858. It's the oldest university in Japan. It was founded in 1858. The highest bill in this country is 10,000 yen on paper. This person is the founder of Keio University. The founding member of the modern Japan... that's basically what he did.

Meiji era started in the 1868. Our university was founded 10 years before that. It was at the end of the Shoden era.

I was working on the internet. Kaizen is the main title of this conference. But I came from the Internet space or industry. Keio University has been known for their very strong development of the Internet both in Japan and Asia as well.

Do you know when the Internet was established or boomed? When was the Internet formed? 1979... 1960... I will get into that.

This is a book written by our university's founder. He visited the United States in 1864. He wrote this book after. "Affairs in the Western countries by Yukichi Fukuzawa" 1866.  That time in Japan, was not the same. He saw the telegram and the testing of that in 1884. He created this picture of a connected planet with poles covering the globe, and then the carrier running across the carrier lines and wires. He made this image already, that the world is going to be connected. And the person running on the wire is what we call an internet packet ((laughter)). This was a great vision, and we're living in it.

We call it the internet civilization. Why? One way of looking at civilization is that, society and civilization is tightly coupled. Culture and civilization. Technology and civilization, is important source. Geography is all meaning- the Africa, and Asia, so geographies is important.And the segment of civilization- because the geography is different and multiple civilizations existing together on the planet.. and therefore conflict.

We read these as cyber space. Cyberspace was created by science, mathematics and other logics. Society created on top of the internet, culture and technology and supporting the internet and then our civilization is growing by technology. Our chairman said bitcoin is a global industry. Do we care about the geographical differences? You are traveling around, you are visiting Japan.

Do we have multiple internets? No. We have The Internet. It's capitalized. Single entity. As far as you, you are on the Internet, and you are connected. Conflict of civilization? We hope we don't have a conflict- but we do, with the existing real space things. So that's what I'm talking about.

Before getting into that, let me review the history of the internet. 1969 is important for two reasons for the origin of the internet. One is the unix operating system. And the second is ARPAnet. The reality is that UC Berkeley distributing TCP/IP and therefore global internet exists. Whatever your favorite operating system is, it originated from UNIX. It was the first operating system for human beings and users, not for the vendor's hardware staff.

I have classified each of the periods in the development of the internet into different categories. UNIX, ARPAnet, TCP/IP was the technology phase. In the 90s, it was the business phase. In the early 2000s, it was the security phase with internet neutrality, y2k, etc. In 2007-2012 it was all about users. From 2012-2016 it was all about data. 2017 and onwards, I think it's about trust.

Some of my students don't know about y2k ((laughter)). There were newspaper articles saying the internet was going to be destroyed by attacking the root servers. If you don't have DNS, then that's a single point of failure to destroy the internet. That was on the Washington Post as a cover story. I told them, no, we have a distributed system around the world. We don't stop it.

If you are isolated from the United States, you are going to die. Your economy relies on the internet already. If you are isolated, then you will die. There's a routing algorithm. That was around in 2001 discussion. Security was becoming very important.

By the introduction of the smartphone, bitcoin, and others, it became all about users. It's about users, data and trust. Those are the very broad view of the history of the internet.

I want to talk about Vint Cerf, Bill JOy, ... Bill is my good friend who started Sun Microsystem, and Jon Postel, ... we worked together for the domain name systems. Stephen Wolff... do you know this person? He was the head of the National Science Foundation. I was working on TCP/IP at the time for general connectivity. The machine was at Mt. Fuji and we were piggy-backing on cable sponsored by another organization. We transferred IP on top of it. At that time, the Japanese government said no no no, the telephone communication should be done by a government company and you're trying to the connect the Internet or ARPAnet... and they realized it was a military project and it was dangerous and therefore you shouldn't be connected. But we were already connected. I told Stephen at NSF I said everyone in Japan was worried about connecting to ARPAnet therefore it's a military thing and therefore it's dangerous and they don't understand. He left the room for 3 minutes, and then he came back. "In light of our discussion this afternoon, on behalf of the NSF, it is a pleasure to grant Internet access to the Japanese IP community. Sincerely, Stephen Wolf". He instantly typed this letter and then he asked me, does this help? I said, thank you. I showed the letter to everybody, and I said the internet is okay. I told politicians, and the government of Japan. I met Stephen last year and I said you started very official open activities of Internet in Japan. I told him and he said, if this year, I'm going to be in jail, that's what he told me.

The global internet was developed under complex situations like that. Okay, this might be interesting. In the year 2000, 6% of the world population was connected to the Internet. At that time, the Internet community in Japan was still developing. This year, it's 56% of the world population. This was last year. The U.S. has 95%. Japan 87%. Europe 85%. Everybody is using the internet. Asia is only at 48.1% connectivity. So 50% more people are going to join the internet including China and India. When you are developing for bitcoin, keep in mind that there's 50% more population from Asia joining online that have never had internet access before.

I want to talk about cybre space and real space. There's cyber space and real space. Internet space, we can do most of the things now. In real space, we have nations. Bitcoin is a global entity. The Internet is a single space, connecting multiple cultures, languages, nations, and laws, and courts.

The Internet is a truly global space. We don't care about anything except IP transmission. Bitcoin is working within the Internet space. There are different regulations in different nations. Anything you do on the internet is going to run into these issues.

I want to talk about Tokyo. This is a picture of a new taxi cab. If you have a taxi waiting for you, and if you find the third taxi in this shape, get on this. Don't ride on the other ones. This is a hybrid taxi. It's an electric hybrid car created by Toyota. This is going to be more than 90% of the taxi cabs in this country by 2020. There's a lot of batteries in there.

Talking about batteries, we're working in a battery society. Creating big batteries that are safe and integrating them into buildings... you all have smartphone batteries and they are everywhere. We have been creating layered batteries and trying to make them big and safe. After 5 years of development, we have achieved that. In this work, we have AC/DC conversion and that is going to be losing.... this is about the supply of electricity and it's really important. You have an AC adapter for your computer, and you convert it, and then you move it. In this country, every single ground station ... after an earthquake in 2011, all the power gone. The internet worked for 3 hours.  Everywhere in this country has 3 hours of battery or 24 hours of battery in a tri-grid groundstation. It has a 24 hour battery. We already have battery distributed around the nation.



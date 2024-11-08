---
title: Extracting Seeds From Hardware Wallets
transcript_by: Bryan Bishop
tags:
  - security-problems
  - hardware wallet
speakers:
  - Charles Guillemet
media: https://www.youtube.com/watch?v=wiA1bT4ObVo
---
7DC5A359D0D5B5AB6728...

<https://twitter.com/kanzure/status/1137672946435198976>

## Introduction

My talk is about extracting seeds from hardware wallets. I am chief security officer at Ledger. I joined Ledger a bit more than one year ago. I built the Ledger Donjon which is an independent red team. Our mission is to help secure Ledger's products. So what we do day to do is try to break all the hardware wallets. We continuously challenge the security of our products. From time to time, we also provide 3rd party security services. We focus on sidechannel analysis, software attacks, perturbation attacks, and cryptography. We feel we have a responsibility to enhance the security in the whole ecosystem. We have also open-sourced our attack tools. Pull requests welcome.

<https://github.com/Ledger-Donjon>

## Ellipal: "An airgapped wallet using Trustzone"

This was called Ellipal. It was an interesting target because it had no wifi, no bluetooth no nothing. The only way to communicate with the device is by QR code. So you either scan a QR code from its screen, or you display a QR code to its camera. In order to upgrade the device, there is an sd card slot. The security model is quite simple. To unlock the device, you enter your pattern. When you want to make your transaction, you input your own password which is supposed to decrypt your private key.

SWo we ordered our Ellipal and waited for it... meanwhile we looked at the upgrade mechanism which uses an sdcard. You have to put the upgrade .bin file into the sdcard and this is a binary file that is encrypted and signed. Uh, so let's check these. So we bruteforced the URL of the ellipal servers in order to find the different binaries

<https://order.ellipal.com/lib/v2.0.zip>

<https://order.ellipal.com/lib/v1.7.zip>

It did not seem to be well-encrypted. They were using 64 bits encryption, so it seems like they are doing encryption in ECB mode. If you know anything about cryptography, ECB mode is not a good idea. So we launched hashcat on our GPU and in order to bruteforce a DES key in hashcat you need like one week or something like that.

Meanwhile, we received our Ellipal and we played with it, and found some hidden menus. We opened the device and noticed there's a metal shield, so we removed the shield and then we looked at the electronic components. There's USB for charging the device; and it's not connected for data. There was an externa lflash- a physical dump is possible by removing the trip and reading what's inside if it's not encrypted. There was also this MT6580A Mediatek SoC which is a low-end SoC for mobile phones usually. It's based on Cortex A7 and it has an ARM MALI GPU running at 500 MHz. There was bluetooth and wifi and so on.

We probed the UART interface which we noticed was present. We probed the two wires. When the device boots, there's a lot of stuff that goes to this wire and givces interesting information on what's inside. We also played with the transmission wire and we sent a FACTFACT on the tx wire which is about factory mode. Then the device went into factory mode and we were able to get wifi and connect to our network. We were able to check and see that wifi was still activated.

What about the usb? It is not physically connected. But there's pin points on the PCB so we just had to solder the USB data to the pinpoints. Then I used mediatek\_flash\_tool after connecting the USB port to our computer. We used the mediatek bootloader and we were able to use the mediatek bootloader. We had full access to the flash memory, and the filesystem was not encrypted. We were able to enable non-root ADB, install third-party APKs, you're root on an android system. It is possible to backdoor the wallet, reactivate wifi, everything is possible.

We got a dump of the wallet application and began the reverse engineering process. We retrieved the firmware signature public key, and the firmware encryption key (3-DES) that we had tried to bruteforce. The bruteforce had not succeeded because it was 3-DES... we also retrieved the encrypted wallet.

We studied how the encryption mechanism was implemented. It's a mess. They used a simple sha256 to hash your password and this mechanism they use to decrypt the key of your wallet.... your password can be bruteforced without GPU in a few minutes. 8 full random character password in a few minutes on GPU. If you have physical access to an Ellipal device, you can reactivate the USB port and then get access to the data.

On their website, they list some security features but here's the reality. For example, they claim that they use TrustZone but they don't. They also claim "AES 128 high-intensity". I have no idea what that means. They also claim they have high quality entropy generation, but they actually use the standard calls to android's random number generator.

We recently disclosed this to Ellipal 3 months ago and we have a very good relationship with them. They have updated their device, they even went to Paris to visit us. We talked with the design team and it was cool. They said they have updated to v2. We didn't check that, I have no idea if it is well-patched. But it also triggered a bug bounty program at Ellipal. They also sent us a small bounty reward, so thank you for this. They also issued a press release saying thank you to Ledger, so thank you as well.

## Sidechannel attacks to extract PINs

I am going to present two different attacks, one is guessing the PIN and the other is extracting the seed. This first one is about Trezor, it's a very similar design to Trezor. Usually sidechannel attacks are very difficult to implement. The microcontroller it was using was not designed for sidechannel security. You can measure the power consumption of the device during its computation and try to figure out if there's a correlation between the data in the device and the power utilization. If there's such a correlation, then sidechannel attacks can exploit this to exfiltrate data. The typical setup is the device hooked up to an oscilloscope and the computer that talks to the hardware wallet.

The code counts the digit and compares to the current value stored in flash memory. So we took a trezor device and we sent a lot of different random PINs and tried to figure out if there's a correlation. As you can see on the trace, the peaks correspond to a correlation between the power consumption of the device and the value of the stored PIN. When there's a correlation, then we need to figure out how to exploit it.

One way is to use machine learning techniques, like the same kind that recognize cats or dogs in pictures on the internet. So you feed you rmachine leanring algorithm with a bunch of photos of cats and you train it with labeled data sets. We can do this in a similar way with digits of pins. So you get a device together where we know the behavior of the power consumption of the device as a function of the value of the digit. On the second device, we get physical access to the attacked device, and you enter a random PIN, measure the power consumption of the device, then ask the machine leanring algorithm what is the most likely value of the PIN. Then you try the PIN on the device, if it's correct you're finished. If not, you try the second choice. You have more information that ytou will use and feed into your machine learning algorithm. On average, 5 tries are enough to guess the correct value of the PIN. On trezor, you have 15 tries, so this works all the time.

We responsibly disclosed this vulnerability back in November 2018-11-20. I think sidechannel attacks are still possible to break, but unlikely that within less than 15 choices that you can break. So the device is going to get wiped before you can guess using another technique we think.

## Extracting seeds

We were able to extract seeds from Trezor One, Keepkey, B walle tand Trezor T. This is unfortunately not patchable. It can be done on every firmware for now and in the future too. We decided to not disclose the method, to protect users. I think this is quite responsible. But we have been asked for more details. I'll give a few details.

Physical access is necessary. The setup cost is around $100 per computer. The necessary time is 3 minutes of prepatration and 2 minutes for extraction. We have a magic back box which we call an extractor, and it takes two minutes to extract from the device. It works on every firmware version. The extraction depends on PIN length. We wrote a program called ExtraKtor.

We suggest using a very long passphrase. We disclosed this to Trezor on 2018-12-20. It can't be patched. The suggested physical threat is out of the threat model; so try to make sure your hardware wallet is not stolen. You need at least 36 random characters.

At the end, they gave us a bounty for this. So that was cool. Thank you. They also thanked us in a press release and stating that we did this.

## Shamir secret sending

The last attack is Shamir secret sending. Take a look at the HTC Exodus phone. This is a "native web 3.0 blockchain phone", I don't really know what that means but it has a "hardware wallet" and a "trusted display" and it has a social key recovery technique. They use Qualcomm SnapDragon 845 SoC. So probably a good phone, right. The general scheme of trustzone here is that there's a Zion app and the seed is stored in the seucre OS. They have a social key recovery method.

We studied the social key recovery which is an interesting function. When you want to backup your seed, they found an interesting method where as a user when you generate your seed you choose in your contact list what they call "trusted contact" and you will ask them to install the Zion app that HTC developed. When you generate your seed, your trusted contacts will receive a share. This is a 3-of-5 share. 3 shares are necessary to reconstruct the seed. The shares are not stored securely in your trusted contact's phones, but it's not important because if the attacker is going to be able to get 1o r 2 shares it doesn't give information about the seed. You need at least 3 shares, so it's not a problem.

This uses shamir secret sharing. When you generate your secret, you also generate degree-2 polynomials. You will evaluate this polynomial at 5 different points, and these 5 different points will be the shares that you send to your trusted contact. Thanks to Lagrange's theorem, only 3 shares are necessary to retrieve the value of the polynomial and then to evaluate it and retrieve the secret. This is a really nice scheme and it works perfectly.

We took the HTC android application and did some reverse engineering in order to understand how it works. They implemented Shamir secret sharing by sharing the 256 bit seed (32 bytes) with 32 different polynomials of degree 2, and then it evaluates it in 5 points and sends the shares. The coefficient a,b are randomly generated with a PRNG and must be kept secret.

The problem with HTC's implementation is that the PRNG update operation is linear and not updated well. Both a and b are linearly dependent. Instead of ending up with a polynomial that they expected, they end up with a different one which has a linear dependency between the coefficients.

When you want to extract your secrets, you either use Lagrange's theorem which works perfectly but you can also put your problem in a system of linear equations. Then you have to solve a linear system of 768 equations over GF(2). When you have three shares, you have 768 unknown and.... anyway, the system is not linearly independent and the rank of the 768-bits matrix is not 768 but it is less than 512. That means that using 2 shares, the kernel of the matrix can be computed in less than 1 second and this seed can be extracted. You only need to compromise 2 different trusted contacts, then you get their shares and you're able to get the seed.

So one trusted contact can collude with another and retrieve the value of the seed. This is really bad.

In firmware v1.54.2401.6, the PRNG is seeded with a fixed value. By reverse engineering the application, we know the value, so it's easy for us to calculate a and b polynomials. So only one share is enough to compute the seed. This means a malicious application can extract YOUR seed from the phone of any of your trusted contacts.

Instead of shamir secret sharing, they implemented shamir secret sending.

We recently disclosed this to an HTC security team. They patched it quite quickly. But the users have not been warned which is a problem, and users have not been encouraged to re-generate their seeds. If one of the trusted contacts are still on an old version of the Zion app, the seed is inside of there. It's definitely a problem. It triggered the creation of a bounty program for the Zion vault. They announced their bounty program in a press release.



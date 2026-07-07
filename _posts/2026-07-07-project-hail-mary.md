---
layout: post
title: Project Hail Mary
date: 2026-07-07 13:13:06 +0000
categories: development
permalink: /project-hail-mary/
---
I loved this movie for how inspiring it was - meeting Rocky and thriving against all odds. It was a brilliant piece and made me reflect on what it means to be human. The software that Ryland used to communicate with Rocky caught my attention with how it cultivated a strong relationship. I would like to reproduce it.
It reminds me of Shazam, Ryland's algorithm must be fingerprinting words and then finding closest matches. I don't think it's machine learning because there was no training period, just assign a sound bite to a word and then it would recognise the sound bites in the future.
Fortunately Avery Wang of Shazam has published a paper on the technology behind Shazam so let's give it a read https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf
# Notes
- each audio file is fingerprinted
- features of the fingerprinting algo:
- robust
	- spectrogram peaks, peak is candidate if it has a hgiher energgy content than all its neighvbors in a region centered around the point
	- chosen accoriding to density criteion, ensures time freq strip has reasonably unifor  coverage ?
	- Peaks chossen are the highest amplitude peaks
	- eq = equalisation?
	- "gsm encoding", global system for mobile communications, because their product was intended to be on a phone. I don't need this le
- temporally localized, translation invariant, robust and sufficiently entropic
![[spectrogram.png]]
Spectrogram normally shows 3 features of an audio bite. For 2D frequency and time are given as axis then amplitude is given as how deep the colour is.
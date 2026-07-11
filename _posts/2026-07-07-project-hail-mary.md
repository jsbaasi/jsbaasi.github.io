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
	- "gsm encoding", global system for mobile communications, because their product was intended to be on a phone. I don't need this level of robustness tbh, I have a bit more data to work with to produce slighly more accurate results?
- temporally localized, translation invariant, robust and sufficiently entropic
![[spectrogram.png]]
Spectrogram normally shows 3 features of an audio bite. For 2D frequency and time are given as axis then amplitude is given as how deep the colour is.
- After how much processing exactly does shazam search the database?
- so it seems like they developed the algorithm, then decided to test it on a bunch of tracks and recorded how many true/false positives true/false negatives they got then this decided their significance level for a track. I'd assume they allowed some false positives? I'm not sure on this but I'd assume that I would want the same level
- figures 4 and 5 show recognition rate trending towards 100% when the signal to noise ratio (snr) increases. Longer tracks needed a lower snr to be recognised 100% which makes sense logically
- some statistics analysis on the advantages of forming pairs instead of searching using individual constellation points, this is working out the tradeoff of spectrogram peaks surviving from the transformation between source material that plays (in our case the person speaking) to the recorded audio bite. they traded off taking 10 times as much hashing points (10 times pairs as there would've been single points) for 10000 times the speed and small loss that the spectro peak gets detected
- but i didn't get any of this statistics analysis tbh
- machine learning does this kind of thing by learning which features are statistically significant, we are essentially telling our algorithm which features are important to us.
# DSP Notes
- microphone just samples the air pressure at multiple points in time
- fourier transform is as follows:
- imagine a signal plotted on a graph, time as a function of amplitude, and suppose this signal had a frequency of 2hz, 2 beats per second. then wrap this function around a singular, distance away from the point being the same as the distance away from time axis to the function on the signal graph. then with this wrapping function we have a variable to decide, how fast do we wrap the signal function? if one cycle is a full rotation for the wrapping function then let's set this to 2 cycles. let's introduce another variable, weighted average of the wrapping function's x points. what you'll see now is, when you set wrapping function to 2 cycles per second (cps) then there's a spike, if we set this to 0.5 or 4, it's pretty much at the origin. which makes sense because the cps doesn't line up completely with the signal frequency to the point where the peaks and troughs balance one another out, as opposed to 2cps where the peaks contribute together to one direction and troughs to the other, this results in a spikey average. we can plot the winding frequency as a function of amplitude, and what we see is that there's a peak at 2 and then flat noise the rest of the winding frequency, so when there's a peak in the winding frequency it means that there's a component of the signal that is cycling between peak/trough at the frequency. so the power of this process is seen when we analyse a signal that has different frequency signals combined together, when changing the winding frequency we can detect the signal frequencies present, a way to extract information from a signal graph
- https://en.wikipedia.org/wiki/Welch%27s_method this describes chunking the time domain signal, fourier transform to the frequency domain and then graph the chunks. it also describes overlapping chunks to reduce signal loss
# ok so what exactly am I doing?
- this differs from shazam as it's live audio, is there any considerations to make there?
	- shazam works on longer audio duration, below I've suggested using 2 seconds runway but maybe we'll need more to use this algo? This algo is optimising the searching process across the database then accuracy then latency of results returned I guess, so if I was to implement it then it would be great with lots of words registered, but really I think I want accuracy first then latency then searching process? idm making all kinds of pre-computations
	- i think the biggest is that this is music and we're going to be working on recognising words, fundamentally there's not many extreme frequencies, words are shorter. I think we need more accuracy. I think the field of DSP has figured out more accurate ways to recognise words for sure
	- the overlapping style of speech that humans use makes it hard to piece out words. other common problems such as vocab size and different speakers doesn't apply to the software from the movie
- have 2 modes: conversation and registration
- in conversation you can keep talking and if a word is not recognised then it is prompted to the user to enter registration mode and write what word it is.
- in conversation mode we record a stream of audio and lop off the biggest match we can find so far maybe? but like "talking" could be recognised as "tall" "king", how do we avoid that? I guess we have a delay between chunk of audio stream processed and word written on screen? so the longest word really would be like 2 seconds max then we move a sliding window of 2 seconds, and find the longest word that could match this audio bite, lop off this word and then start the window from the earliest un-recognised portion of the audio stream, in the movie there's roughly a 1 second delay between rocky speaking and it being recognised so could work and perhaps we make some optimisations later
- recognition algorithm:
	- make a spectrogram by fourier transform
	- reduce spectrogram to constellation map
	- 
- ![[recognition.excalidraw]]
- 
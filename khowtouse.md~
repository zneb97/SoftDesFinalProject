---
title: How To Use
layout: template
filename: khowtouse
--- 
# Getting Started

Of course, the first thing to do to get started running libROSA on your own is the clone the BACLaudio project at https://github.com/audreywl/baclaudio 

The main external library that we are using to do analysis is called libROSA. libROSA has a ton of dependencies, which can be obtained by executing

```
$ sudo apt-get install python-numpy python-matplotlib python-scipy libpng12-dev libfreetype6-dev libav-tools libsamplerate0-dev
```

at the command line. Then install libROSA and one more dependency with

```
$ sudo pip install scikits.samplerate

$ sudo pip install librosa
```
To start the visualizer, simply run wrapper.py. 
```
$ python wrapper.py
```
It will prompt the user with what song they want to visualize. If you haven't downloaded a lyric and audio file for yourself, try Hallelujah by Rufus Wainwright, Bad Reputation by Joan Jett, or The Best Years Of Our Lives by Baha Men, which come with the repo.

It is highly likely that you will get the following error every time you run the code:

```
	/usr/local/lib/python2.7/dist-packages/matplotlib/font_manager.py:273: 
	UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.
```

To fix this, in the python interpreter, run

```
	import matplotlib as mpl
        font_cache_path = mpl.get_cachedir() + '/fontList.cache'
        %rm $font_cache_path
```

The first time the code is run, the error may return, but it should not from then on.



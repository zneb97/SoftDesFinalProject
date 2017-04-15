---
title: About Our Code
layout: template
filename: jaboutourcode
--- 
# Code Architecture
Our code is comprised of a series of classes.  Our uppermost class is View, where all the parts of our visualization are drawn in a pygame window.  View knows what to draw from Model, where all of the dots are initialized. 

Model is where most of the other classes interact with each other.  Analysis of the music is done in the music using Song, which uses Channels to create a standard format for storing data.  From Song, we can pull out the lyric sentiment and the current chord, which are used to set a color from Color_Gradient and a function path from Functions.  Dot stores everything a dot needs to know so it can update independently after it is initialized.  Song also provides the times beats occur, which is when a Dot is created.  A Dot stores everything it needs to update itself independently after it is initialized, including its specific color and function path. Paths uses Functions to create lists of points that represent the different paths a Dot can follow and get drawn in the background during View.
![Our UML Diagram](https://raw.githubusercontent.com/audreywl/baclaudio/master/Final_UML.png "Our UML Diagram")

---
title: The Code
layout: template
filename: codeAbout
---
# Code Architecture
![Code Module](https://github.com/zneb97/SoftDesFinalProject/blob/gh-pages/resources/CodeArche.png)

Our code is broken up into two main components, the feature extraction code and the neural net, which reads from and makes decisions from the data of the feature extraction. Both of these are implemented directly into the base pygame code, allowing us to avoid the problem threading and quickly interact with features.

## Feature Extraction
![How it Works](SoftDesFinalProject/resources/Team AFK.png)

Using the pygame's board object which uses a more basic numbering system for each kind of tile, we created our own grid object with better values for distinguishing all possible tiles and what may be located on the title.

![Grid Strategy](https://github.com/zneb97/SoftDesFinalProject/blob/gh-pages/resources/Input%20Graphic.jpg)
In addition to this, we pad the newly created grid with zeros while shifting it relative to the player's movement, allowing us to always keep the player (designated by the number 8 in our grid), in the same spot in the matrix. This greatly cuts down on the computation needed. Rather the spend O(n<sup>2</sup>) searching the entire matrix for the only 8, it only takes O(1). This allows us to get the surrounding tiles just as fast, which are the features we feed into the neural net.


## Neural Net
![Machine Learning](https://github.com/zneb97/SoftDesFinalProject/blob/gh-pages/resources/Team%20AFK%20(2).png)
To implement the neural net, we used the open source and widely used TensorFlow library, allowing us to pass in the extracted features, which are then considered and combined to weight the six possible commands and ultimately chose one for the Bomberman to perform.

Based on the way we implemented the neural net, the computer currently
has the primary objective of surviving. In the future we hope to change this instead
to clear levels.

![Machine Learning](https://github.com/zneb97/SoftDesFinalProject/blob/gh-pages/resources/Team%20AFK%20(1).png)
Based on the titles around it, the Net always keeps track of what decisions in can make, whose probabilities are influenced by three categories: bricks, bombs, and enemies. The weight, or how much influence each of these categories has on the final decision varies based on the scenario. For example. when a bomb is nearby, movements to protect the Bomberman become more important than destroying bricks.

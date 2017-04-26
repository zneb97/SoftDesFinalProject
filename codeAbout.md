---
title: The Code
layout: template
filename: codeAbout
---
# Code Architecture
![Code Module](/resources/CodeArche.png) <br>
Our code is broken up into two main components, the main game loop and the machine learning module. The game loop is a pygame implementation of the Bomberman game and uses the typical Model View Controller logic. The machine learning module consists of a Feature Extration Module and a Neural Network. Both of these are implemented directly into the base pygame code, allowing us to avoid the problem threading and quickly interact with features.

## Feature Extraction
![How it Works](/resources/Team AFK.png) <br>
Using the pygame's board object which uses a more basic numbering system for each kind of tile, we created our own grid object with better values to distinguish all possible tiles and what may be located on the title.

![Grid Strategy](/resources/Input Graphic.jpg) <br>
In addition to this, we pad the newly created grid with one (the number that represents the wall) while shifting it relative to the player's movement, allowing us to always keep the player (designated by the number 8 in our grid), in the center of the matrix. This greatly cuts down on the computation needed. This allows the neural network to access the grid information surrounding the player relatively quickly.

## Neural Network
![Machine Learning](/resources/2.png) <br>
The neural network module reads extracted feature data from human players and saves a neural network for future prediction. While the game is running in AI mode, it receives live features and predicts the movement with the saved data.

Based on the titles around it, the Net always keeps track of what decisions in can make, whose probabilities are influenced by three categories: bricks, bombs, powerups and enemies. The weight, or how much influence each of these categories has on the final decision varies based on the scenario. For example. when a bomb is nearby, movements to protect the Bomberman become more important than destroying bricks.

![Machine Learning](/resources/1.png) <br>
Based on the titles around it, the Net always keeps track of what decisions in can make, whose probabilities are influenced by three categories: bricks, bombs, and enemies. The weight, or how much influence each of these categories has on the final decision varies based on the scenario. For example. when a bomb is nearby, movements to protect the Bomberman become more important than destroying bricks.

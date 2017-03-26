**Team AFK  : Bomberman Bot with Machine Learning!**

Ben, Seungin, Nick, Yichen, Alex

**Agenda for Technical Section:**

Today our agenda is to spend five minutes on background and fifteen minutes on our discussion questions. Our background details our choice of game and struggles with our original choice and then subsequent change of game venue. Our discussions are our primary focus on input, machine learning, and servers related technical issues.

**Background:**

![ihatemd](https://github.com/zneb97/SoftDesFinalProject/blob/master/Resource/background.png)

Our project is an attempt to use machine learning to create a bot that plays a video game. Since the start of the project we have already found some important information regarding the type of game and the approach to said game that works best. Our project was inspired  by the MarIO project, in which a machine learning algorithm learns to play Super Mario World through trial and error.

Going off of this we attempted to try to apply this idea to Agar.io, however we quickly ran into several problems. The largest problem was accessing the game&#39;s variables to use as features in our neural net. Whereas the variables can be taken directly from the Super Mario code, Agar.io, being a browser game, the variables were stored on the server side and inaccessible to us. Workarounds we tried included writing our own (too off topic of our main focus), using pygame versions (often incomplete or out of date with current networking libraries),  or using image processing (too slow - takes average of 0.2 seconds to just extract the location of circles, too many variations, off topic from our idea).

Stepping back from Agar.io, we came up with a list of conditions the game we chose needed to have in order to be **feasible** for the scope and focus of our project.

We identified..
1) the need for direct local accessible game data (like player and enemy position)
2) a fixed number of features to feed into the neural net

- --The number of circles (foods, enemies) constantly change.
- --The only constant data is the number of pixels

3) a decently pacing to gameplay

This cumulated in our decision of Bomberman. We attempted to run it off an emulator but due to a combination of poor documentation in memory location for variables and difficulty getting them working with Ubuntu, we ultimately went with a very polished and Wifi accessible open-source PyGame version.

The source can be found here :  https://github.com/rickyc/bomberman-pygame

**Key Topics:**
**1) One Integrated Program (Game + Machine Learning)
    Vs. Two Simultaneously Running Programs(~6 minutes)**

**Integrated**
- ++Do not have to worry about communication between two programs
- ++All variables are accessed easily
- ++Less delay with receiving and sending data

- --Might reduce frame rate
- --Might cause loss of data between server and client during multiplayer
           (which is very bad)

**Simultaneously**
- ++Easier to write, don&#39;t have to mess with base game
- ++Machine learning part doesn&#39;t interfere with the actual running game

- --Might have difficulties grabbing data from base game(due to delay)

- --Issues with multi-threading and technical difficulties associated with the implementation
 |

**2) How should our input look like? (~6 minutes)**

One large question is the implementation of Neural Networks with different categories of blocks. Since they typically act on one feature with each node, we might need to make several, such as one for placements of bombs, one for placement of bricks, one for walls, etc. One of our key questions is the proper implementation of different machine learning programs. Our current preliminary choice is that of a neural network due to its variety of learning styles. We plan to have three different computer players: one neural network that has learning based on human player&#39;s choices, one neural network that uses a system of rewards and consequences to learn, and one hard coded AI that we design.

![ireallyhatemd](https://github.com/zneb97/SoftDesFinalProject/blob/master/Resource/path.png "Logo Title Text 1")


**3) Multiplayer Connection Issues (3 minutes)**

For the network processing part, we still need to figure out how to set up intercomputer communication between server and client. The given code for bomberman has a multiplayer version that theoretically works across computers, but we have not been able to get it to run outside of localhost (although multiplayer does work when run through localhost). It uses the Net library for python with TCP/IP connection.

***

# Upkeep Scripts 2.0

These are the scripts needed to maintain and update the project as new LoL/broadcast updates come out

***
All four of these take the same arguments

|Argument|Addition|Explanation
|---|---|---|
|-v|Videos|Call to use local videos instead of YouTube|
|-n|Videos to skip| Number of videos to skip in the playlist| 
|-p|Playlist|YouTube playlist URL|
|-u|url|YouTube video URL|

***

## ChampionTrackImage

For adding champion portraits to be tracked on the in-game minimap. If a new champion is added to the game/portrait updated, their portraits must be added to the directory using this script

The usage is simple enough, simply type `$ python championtrackimage.py` and follow the on-screen instructions

First you must find a frame at which the champion portrait is isolated on the minimap. Just like the highlighted champions here:

<p align = "center">
	<img src = "/assets/markdown_assets/isolated_minimap.png" width = 300>
</p> 

Then you must give the name of the champ and the 4 coordinates that result in a 14x14px image of the champion. This is best done through trial-and-error and multiple iterations until the perfect match is found

## CreateMapBase

For creating a map base should you need to support a new minimap. This needs to be done for any new leagues the program supports and acts as a reference for the graphs

The usage is essentially the same as in `championtrackimage`, with the only real difference being that you input the code that you want to attribute to the league. Once you've found the 4 coordinates that cover the minimap, the program will draw up a base map without any champions present.

Call with `$ python createmapbase.py`


## DoubleCheck

This is for making sure that the dimensions of a video line up with the program's dimensions. Used to double check that the program will be cropping images properly

Usage is just like the previous two, all you have to do is check if the pictures line up as you would expect


## Stripportraits.py

For stripping champion portraits from the sidebars. These portraits are used for identifying the champions at the start of the game. 

Once you have found a frame with all champions at level one, you must fill in their position's number and name and their portrait will be added to the db

Numbers: 
* 1  : Blue side toplaner
* 2  : Blue side jungler
* 3  : Blue side midlaner
* 4  : Blue side ADC
* 5  : Blue side support

* 6  : Red side toplaner
* 7  : Red side jungler
* 8  : Red side midlaner
* 9  : Red side ADC
* 10 : Red side support

***
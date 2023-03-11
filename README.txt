== Notes ==

The indexer will only run files and not files within a zipped folder.

To change where the indexer runs you have to change the path in the create_index function "target_pages += \FILEPATH".

Note that for linux systems you will use / instead of \\.

This is currently set up to read from the dev folder on a windows system.

== Running the Code on Windows ==

1. Create the index by running indexer.py.

2. Start the search interface by running searcher.py.

3. There will be a text prompt in the console where typing 0 leads to the console prompt, typing 1 leads to the local GUI, and typing anything else leads to a repetition of the prompt.

== Console Search ==

1. First, the prompt will ask if you want to proceed from the console. To quit, type the character N or the character n and press enter. To continue, type the character Y or the character y and press enter. Any other responses will lead to a repetition of the prompt.

2. Type the query. Press enter and the results of the query will be printed to the console as links.

3. The text prompt will then ask if you want to proceed. To quit, type the character N or the character n and press enter. To continue, type the character Y or the character y and press enter. Any other responses will lead to a repetition of the prompt.

4. Steps 2 and 3 will repeat as long as Y/y has been pressed.

5. Once N/n has been pressed, the average time of all of the searches will be printed out.

== Local GUI Search ==

1. The local GUI is small and gray. It was made using tkinter and it may appear behind other things, but it can be brought to the front by pressing the tkinter icon which appears on the start menu and looks like a dark blue feather.

2. There is a white box in which queries can be typed. In order to enter a query, type a query into this box and press the button to the right which says "Enter Query". Pressing enter on the keyboard does not work in the local GUI and will do nothing.

3. The urls of the results will appear at the bottom of the GUI. In order to find other results, repeat Step 2 after deleting the previous prompt. To stop searching using the local GUI, press the "X" on the top right of it.

4. Once "X" has been pressed on the GUI, the average time of all of the searches will be printed out.

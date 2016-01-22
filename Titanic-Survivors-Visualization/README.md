SUMMARY

This data visualization is based on the Titanic survivors data. Its key
message is to show that women and more affluent passengers were more
likely to survive the Titanic disaster.

The live webpage for the final visualization is hosted here:
http://embed.plnkr.co/woBbwOXQHLyOvTGviDB4/

DESIGN


(1) index1.html - INITIAL DESIGN

As the variables are categorical I chose to use bar
charts. To show the relative proportions of survivors vs victims for
each category, I decided to use stacked bars.

I used Pclass for the x-axis and Sex as a series on the storyboard. This
was a somewhat arbitrary decision as I could have switched the 2
variables around (i.e. Sex on x-axis and Pclass as storyboard series).
In any case, Pclass has more categories than Sex, so
that gives me more information per frame, so I decided to stick with
this arrangement.

I used a measurement axis rather than a percentage axis to
show the counts of survivors vs victims. The stacked bars and relative
proportions of the different colors would serve the same purpose as a
percentage axis in illustrating the distribution of survivors/victims
for each Pclass. The measurement axis would also provide more
information than the percentage axis, i.e. on the relative sizes of
total passengers per class.

I also made some aesthetic choices to change default settings for color and font
for better readability.


(2) index2.html - REVISIONS AFTER FEEDBACK (1)

Incorporating Feedback (1) below, I changed the color
encoding for "Perished" to red. I also incorporated functions to pause
and resume the animation with clickable indicator bars for Sex. 

The indicator bars allow for pausing of the animation and selection of a specific frame,
so this helps to resolve the problem of the reader being unable to keep up with the animation.
The category for the current frame shown is also highlighted a different color on the 
indicator bars. This shows the current frame being viewed and allowed me to remove the
confusing storyboard titles. 

I also made a change to the legend so that it would not refresh between frames as that 
was disturbing to readers. 


(3) index3.html - REVISIONS AFTER FEEDBACK (2)

Incorporating Feedback (2), I changed the color of the
selected indicator bar so that it was more striking (but not too garish). 
I also made the indicator explanatory text and
indicators more visible. The relative sizes of the main chart
and indicator chart were tweaked so that it was clearer which frame of the story was
being shown.

I moved the indicator chart to the left of the
visualization. As our eyes tend to scan visual material from left to
right, I felt that this change would make it clearer to readers that
there was an option to pause the animation.

I also increased the frame duration.

The "Survived" bars were repositioned to begin at y = 0.


(4) indexfinal.html  - FINAL REVISIONS AFTER FEEDBACK (3)

Incorporating Feedback (3), I fixed the y-axis scale so that it doesn't change 
from frame to frame.

I also added an explanation about what Pclass meant.

Final edits to the layout of the different elements were made to make the visualization
clearer.



FEEDBACK


1) Comments on index1.html: 

"Color encoding for "Perished" could be more eye-catching, e.g. red"

"Frame duration is too short, I didn't have time to finish reading or look
at legend" 

"I couldn't distinguish storyboard titles from main heading"



2)  Comments on index2.html: 

"Indicator bars are not obvious enough, I needed time to figure out how to pause the animation"

"Color encoding for selected indicator bar not obvious enough"

"Animation changes too fast" 

"I'm more interested in the number of survivors so would prefer to
have them depicted from the y=0 baseline, so that I can immediately get a sense
of the numbers"



3)  Comments on index3.html: 

"What is Pclass 1, 2 and 3 and how do they relate to affluence?"

"The y-axis scale changes between frames so it's quite misleading, it looks as though
there are comparable numbers of males and females"

"The orientation of colors for the bars and the legend are different i.e. red/top, blue/bottom
for bars and vice versa for legend. This makes it a bit confusing" 



RESOURCES
1) http://dimplejs.org/advanced_examples_viewer.html?id=advanced_storyboard_control 
2) http://tutorials.jenkov.com/svg/text-element.html#positioning-text
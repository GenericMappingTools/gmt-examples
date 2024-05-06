How to use colors in GMT
------------------------

In GMT you will want to define the color of different feautures (line, symbols, polygones, text, axes, etc.).
There six methods to define a color:

* colorname
* R/G/B
* #RRGGBB
* Graylevel
* H-S-V
* C/M/Y/K

Color names
~~~~~~~~~~~

This is more friendly way to define a color. There are 663 unique color names that can be select. 
All names are case-insensitive. You can see the names (and its RGB values) in this link. :gmt-module:`coast`.
For an interactive color picker, see :doc:`color-picker`.

   .. gmtplot::

      gmt begin frames png
         gmt coast -R-180/180/-60/60 -JM25c -W
      gmt end show


Color models
~~~~~~~~~~~~
Alternative, you could use one of the following five color models to define a color. 
These are mainly useful when, for example, you want to have the exact same color that you see on internet.
There are five models color accepted by GMT. GMT automaticly identifies the model based on the sintax.

R/G/B model: 
===========

Provide 3 values each from 0 to 255 separated by a /.
Specify Red, Green, and Blue levels. Each value is separated by a slash and is in the range from 0 (dark) to 255 (light). This representation is used to color monitors.

#RRGGBB
=======

Specify Red, Green, and Blue levels in the way that it is done in HTML. Use two characters for each color channel, ranging from 00 (dark) to FF (light). Upper and lower case are allowed.

Graylevel
=========

Specify a single number from 0 (black) to 255 (white). It only uses shades of gray (R = G = B). This representation is popular with black and white printers.

H-S-V
=======

Specify Hue in the range 0 to 360 (degrees), S saturation between 0 (not saturated) and 1 (fully saturated), and value V between 0 (dark) and 1 (light). Number are separated by hyphens. This representation can be helpful when hue varies a lot.

C/M/Y/K
=======

Specify Cyan, Magenta, Yellow, and blacK. Each number is in the range from 0 (no paint) to 100 (maximum paint). This representation is used by most color printers.

   .. gmtplot::

      gmt begin frames png
         gmt coast -R-180/180/-60/60 -JM25c -W
         gmt basemap -Ba30f7.5g15
      gmt end show


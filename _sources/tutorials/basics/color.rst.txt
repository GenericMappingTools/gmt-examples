How to use colors
-----------------

In GMT you will want to define the color of different features (line, symbols, polygones, text, etc.).
There are six methods to define a color:

* `Color names`_
* `R/G/B`_
* `#RRGGBB`_
* `Graylevel`_
* `H-S-V`_
* `C/M/Y/K`_

Color names
~~~~~~~~~~~

This is more friendly way to define a color. There are 663 unique color names that can be selected. 
All names are case-insensitive. You can see the names (and their RGB values) in this 
`link <https://docs.generic-mapping-tools.org/latest/_images/GMT_RGBchart.png>`_
or use this interactive :gmt-module:`color-picker`.

In the following example, we use ``lightgray`` for the dry areas and ``royalblue4`` for the wet areas.

   .. gmtplot::

      gmt begin color png
	      gmt coast -Rd -JW12c -Glightgray -Sroyalblue4
      gmt end show

Color models
~~~~~~~~~~~~
Alternatively, you can also use color models to define a color. 
These are useful especially when you know the values that define the color you want to use.
GMT identifies the color model according to the syntax used.

R/G/B
=====

Provide 3 values each from 0 to 255 separated by a /.
Specify **R**\ed, **G**\reen, and **B**\lue levels. 
Each value is separated by a slash and is in the range from 0 (dark) to 255 (light).
This representation is used to color monitors.


#RRGGBB
=======

Specify Red, Green, and Blue levels in the way that it is done in HTML. 
Use two characters for each color channel, ranging from 00 (dark) to FF (light). 
Upper and lower case are allowed.


Graylevel
=========

Specify a single number from 0 (black) to 255 (white). It only uses shades of gray (R = G = B).
This representation is popular with black and white printers.


H-S-V
=====

Specify **H**\ue in the range 0 to 360 (degrees), **S**\aturation between 0 (not saturated) and 1 (fully saturated), and **V**\alue between 0 (dark) and 1 (light). Number are separated by hyphens. This representation can be helpful when hue varies a lot.


C/M/Y/K
=======

Specify **C**\yan, **M**\agenta, **Y**\ellow, and blac**K**. Each number is in the range from 0 (no paint) to 100 (maximum paint). This representation is used by most color printers.


Example with color model
========================
It is possible to make the previous map with color models.

Color models for ``royalblue4``:

* R/G/B: 39/64/139
* #RRGGBB: #27408B
* H-S-V: 225-0.719-0.545
* C/M/Y/K: 72/54/0/45

Color models for ``lightgray``:

* R/G/B: 211/211/211
* #RRGGBB: #D3D3D3
* Graylevel: 211
* H-S-V: 0-0-0.827
* C/M/Y/K: 0/0/0/17


   .. gmtplot::

      gmt begin color png
	      gmt coast -Rd -JW12c -G211 -S39/64/139
      gmt end show
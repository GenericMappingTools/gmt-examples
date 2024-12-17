Setting attributes of lines
---------------------------

In this tutorial we will show:

* `Use of lines`_
* `Basic Attributes`_
* `Examples of lines`_

Use of lines
~~~~~~~~~~~~

In GMT, lines (also called *pen*) are used for many features, such as:

* Lines
* Outlines of symbols
* Borders of polygons
* Outlines of text
* Vectors (the line and the outline of the head)
* Map frames
* Scale bars

In the following example, all the colored elements are specified with the pen.

     .. gmtplot::

        gmt begin Pen_examples png
            # Basic frame map
            gmt basemap -R0/10/0/4 -Jx1c -B0  --MAP_FRAME_PEN=thin,mediumpurple
            # Scale bar
            gmt basemap -LjBR+w1c+jBR+l" cm"+o0.4c --MAP_TICK_PEN_PRIMARY=salmon
            # Create Line
            echo 1 1 > tmp
            echo 5 3 >> tmp
            echo 9 2 >> tmp
            # Plot line
            gmt plot tmp -Wthicker,red,...-
            # Plot symbol
            echo 4 1 | gmt plot -SA1c -W1p,orange
            # Plot text
            echo 2.2 3.5 "Hello GMT" | gmt text -Wthinner,darkblue,dotted -F+f24=thin,khaki1,solid -G211
            # Plot vector
            echo 6 1 25 2c | gmt plot -Sv0.3c+ea+p0.5p,deepskyblue -Wthin,darkgreen,--.
        gmt end


Basic Attributes
~~~~~~~~~~~~~~~~

The basic properties of a line are defined by a *pen*.
It has three basic attributes: 

* `Width`_
* `Color`_
* `Style`_


Most programs will accept pen attributes in the form of an option argument, with commas separating the given attributes, e.g.,
``width,color,style``.

**Default pen attributes**: By default they are 0.25-point wide, black and solid line.

Width
=====

There are two ways to define the width:

**Note:** The width of a line will look bigger if the figure is enlarged (and vice versa). 
In this tutorial we add a graphic scale on the figures.

Custom
++++++

Use a number to set the width. Append c, i, or p to specify pen width in cm, inch, or points, respectively.
If not unit is append, them points is used as the unit. In GMT these units are related in this way:

1 inch = 2.54 cm = 72 points


Pen names
+++++++++

You can use one of the following preset names to define its width:

.. _tbl-pennames:

    +----------+-------+----------+-------+---------+-----+
    | faint    | 0     | thin     | 0.75p | fat     | 3p  |
    +----------+-------+----------+-------+---------+-----+
    | default  | 0.25p | thick    | 1p    | fatter  | 6p  |
    +----------+-------+----------+-------+---------+-----+
    | thinnest | 0.25p | thicker  | 1.5p  | fattest | 10p |
    +----------+-------+----------+-------+---------+-----+
    | thinner  | 0.5p  | thickest | 2p    | wide    | 18p |
    +----------+-------+----------+-------+---------+-----+

In the following example we show all the preset names (with differents colors). 

**Note**: In the following examples the ``-Y`` parameter is only used to move the lines vertically. Otherwise the lines would be overlapped. It does not affect the line attributes.

     .. gmtplot::

        gmt begin lines_width png
            gmt basemap -R0/10/0/4 -Jx1c -B0 -LjBR+w1c+jBR+l" cm"+o0.4c
            echo 0.5 3.8 > tmp
            echo 8 3.8 >> tmp
            gmt plot tmp       -Wfaint
            gmt plot tmp -Y-2p -Wthinnest,purple
            gmt plot tmp -Y-3p -Wthinner,blue
            gmt plot tmp -Y-4p -Wthin,green
            gmt plot tmp -Y-5p -Wthick,orange
            gmt plot tmp -Y-6p -Wthicker,red
            gmt plot tmp -Y-7p -Wthickest
            gmt plot tmp -Y-9p -Wfat,purple
            gmt plot tmp -Y-12p -Wfatter,blue
            gmt plot tmp -Y-15p -Wfattest,green
            gmt plot tmp -Y-20p -Wwide,orange
        gmt end 


Minimum-thickness pen
+++++++++++++++++++++

This can be achieved by giving zero width (or faint).
The result is device-dependent but typically means that as you zoom in on the feature in a display, the line thickness stays at the minimum. 


Color
=====
For the color, you can use all the methods explained in 
`How to use colors <https://www.generic-mapping-tools.org/gmt-examples/tutorials/basics/color.html>`_.


Style
=====

The style attribute controls the appearance of the line. 
By default all lines are drawn are solid. 
You can change this by using the following methods:

Names (or symbols)
++++++++++++++++++

You can use some names to get following styles:

* dotted (or ".")
* dashed (or "-") 

Also combinations of dots and dashes, like ``.-`` for a dot-dashed line, are allowed. 


**Note**: The lengths of dots and dashes are scaled relative to the pen width 
(dots has a length that equals the pen width while dashes are 8 times as long; gaps between segments are 4 times the pen width).


String
++++++

For more detailed attributes (including exact dimensions) you may specify ``string[:offset]``. This is a series of numbers separated by underscores (_). 
These numbers represent a pattern by indicating the length of line segments and the gap between segments. 
The optional offset phase-shifts the pattern from the beginning the line.
For example, if you want a thin line that alternates between long dashes (9 points), an 4 point gap, then a 3 point dash, 
then another 4 point gap, with pattern offset by 13 points from the origin, specify 
``-Wthin,9_4_3_4:13p``.
Just as with pen width, the default style units are points, but can also be explicitly specified in cm, inch, or points (see width discussion above).

Here we show some examples of different style lines:

     .. gmtplot::

        gmt begin lines_style png
            gmt basemap -R0/10/0/2 -Jx1c -B0 -LjBR+w1c+jBR+l" cm"+o0.4c
            echo 0.5 1.8 > tmp
            echo 8 1.8 >> tmp
            gmt plot tmp       -Wthin
            gmt plot tmp -Y-7p -Wthin,dotted
            gmt plot tmp -Y-7p -Wthin,dashed
            gmt plot tmp -Y-7p -Wthin,.-
            gmt plot tmp -Y-7p -Wthin,...-
            gmt plot tmp -Y-7p -Wthin,9_4_3_4
            gmt plot tmp -Y-7p -Wthin,9_4_3_4:13p
        gmt end 


Examples of lines
~~~~~~~~~~~~~~~~~

Here we show some examples of lines combining the three basic attributes.

**Note**: In the last two examples the ``-Y`` parameter is NOT used so that the lines are intentionally overlapped to achieve more complex lines.

     .. gmtplot::

        gmt begin basic_lines png
            gmt basemap -R0/10/0/2 -Jx1c -B0 -LjBR+w1c+jBR+l" cm"+o0.4c
            echo 0.5 1.8 > tmp
            echo 8.0 1.8 >> tmp
            gmt plot tmp         -W
            gmt plot tmp -Y-0.2c -W1p,red,-
            gmt plot tmp -Y-0.2c -W1p,blue,.
            gmt plot tmp -Y-0.2c -W1p,lightblue,-.
            gmt plot tmp -Y-0.2c -W2p,blue,..-
            gmt plot tmp -Y-0.2c -W2p,tomato,4_2:2p
            # Complex example of a 5p wide black line with a 2p wide red line above it
            gmt plot tmp -Y-0.3c -W5p,black
            gmt plot tmp         -W2p,red
            # Complex example of 5p wide black line and 4p wide white dashed line on top of it
            gmt plot tmp -Y-0.3c -W5p,black
            gmt plot tmp         -W4p,white,20p_20p
        gmt end
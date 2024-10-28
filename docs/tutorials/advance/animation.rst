Making animations
-----------------

By F. Esteban (@esteban82). October 20, 2024

1. Introduction
~~~~~~~~~~~~~~~

1.1 What is an animation?
=========================

- Animation is a technique used to create the illusion of motion.
- This is achieved by displaying a rapid sequence of still images (at least 12 frames per second).


1.2. How to make an animation?
==============================

- In order to make an animation we need:

#. A lot of still images.
#. Combine all the images in a video format.

.. Tip::
  A video file is just a container format that, when is executed, display all the images in it in a sequential order.


1.3. Why use GMT for animations?
================================

GMT is ideal for animations that require:

- Scientific precision.
- Handling geospatial data.
- High-quality graphical visualizations.

1.4. Types of animations in GMT
================================

I categorize two types of animations based on their complexity in GMT:

1. **Moving objects** (e.g., Earth spinning). It uses the :gmt-module:`movie` module.
2. **Appearing objects** (e.g., earthquakes). It uses :gmt-module:`movie` and :gmt-module:`events` modules.

1.5. Prerequisites
==================

- GMT version 6.1 or later.

2. Tutorial 1. Earth spinning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this tutorial, I will explain the simplest type of animation, 
which only requires :gmt-module:`movie` module. 
As an example, I will create an animation of the Earth spinning similar to the one below:

..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 300px
    :aspect: 1:1

This animation was done from 360 frames (changing by 1 degree the central longitude of the map) which were shown at 24 frames per second (fps). 

Previously, before the movie module was introduced with GMT 6, making an animation like this would require making 360 maps
(1 centred on a different longitude all the way around). For this it would be very useful to use a loop. 
Finally, the figures would be assembled into a video format using ffmpeg or graphics magik. 
You can see an explanation of that times `here  <https://docs.generic-mapping-tools.org/5.4/gallery/anim_introduction.html>`_ 
and some examples `here  <https://docs.generic-mapping-tools.org/5.4/Gallery.html#animations>`_.


2.1. Goals of the Tutorial
==========================

- Provide a general introduction to creating animations with GMT.
- Explain the most important aspects of using the :gmt-module:`movie` module.
- Serve as a guide to help beginners understand and troubleshoot potential issues.

2.2. Step-by-step Instructions
==============================

To create an animation, follow these steps:

#. Make first image
#. Make master frame with gmt movie
#. Make draft animation
#. Make full animation

2.2.1. Make first image
^^^^^^^^^^^^^^^^^^^^^^^

The first step is to create an image using a standard GMT script that will serve as the base for the animation.

**Step Goal**: Create the first image of the animation.

For this example, we will create a map of the Earth with:

     .. gmtplot::
        :height: 300 px

        gmt begin Earth png
            # Plot relief grid
            gmt grdimage @earth_relief_06m -I -JG0/0/13c
        gmt end


.. admonition:: Technical Information

  - **gmt begin; gmt end**: Commands to start and end a GMT script using modern syntax.
  - **@earth_relief_06m**: A remote grid of Earth's relief with a 6-minute resolution.
  - **-I**: Apply illumination to the grid.
  - **-JG0/0/13c**: Stereographic projection with the center at longitude 0 and latitude 0, with a 13 cm map width.


2.2.2. Make the Master Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create animations with GMT, we use the ``gmt movie`` module. 
In this step, we will use it to recreate the previous image (the *master frame*).

.. Important::

  **Step Goal**: Make a master frame that looks identical to the first image.

2.2.2.1. What is GMT MOVIE?
++++++++++++++++++++++++++++

The :gmt-module:`movie` module simplifies most of the steps needed to create an animation 
by executing a single plot script that is repeated across all frames, 
with some variation using specific frame variables.

**Required Arguments:**

- **mainscript**: The previously created script.
- **-N**: Name for the output file.
- **-C**: Canvas Size.
- **-T**: Number of frames.
- There are two type of outputs. A master frame (-M) or a video (-F). You have to asks for at least one of them.

**Optional Arguments** (usefull for this tutorial):

- **-G**: Set the canvas color (or fill).
- **-V**: Show verbose information during the movie-making process.

2.2.2.2. First Attemp
+++++++++++++++++++++

We will create the first frame (``-M0,png``) over a black canvas (``-G``) for an HD video.

     .. gmtplot::
        :height: 300 px

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c
        gmt end
        EOF
        gmt movie main.sh -NEarth -Cfhd -T10 -M0,png -V -L+f14p,Helvetica-Bold,white -Gblack


.. Error::

  - The figure does not fit on the canvas!
  - There is excess space on one side.


.. admonition:: Technical Information

  - The previous script is surrounded by these two lines:

    ::

      cat << 'EOF' > main.sh
      ...
      EOF

  - This saved the main script into the file ``main.sh`` (using a `Here Document <https://en.wikipedia.org/wiki/Here_document>`_). 
  - This is helpfull because allow us to see (and edit) the main script and the arguments of GMT MOVIE just using a single file.


2.2.2.3. Fix the Canvas
+++++++++++++++++++++++

We will fix the canvas size to match the map dimensions:

**What is the Canvas?**

- The canvas is the black area of the previous image.
- This is the working area of the frames. This means that the elements we draw must be inside it.
- Elements that are outside (totally or partially) will not appear in the animation.
- We must compose our plots using the given canvas size.
- The canvas size is important by two reasons:

  - to set the final dimension in pixels of frames/movie (i.e. the quality).
  - set the width and height (in cm or inches) of the frames.

**How to set the canvas**:

- This is set by ``gmt movie -C`` and determine two things:

  - The size of your “plot paper” and 
  - what resolution (in dots per unit; dpu) at which this canvas is converted to a raster image. 

There are two wats to the set the canvas: 

**Presets formats**:

- The easiest way to specify your canvas is to use the presets standard formats.
- Use the name (or alias) to select a format based on this table.


======================= ================== ========= =========
 Preset format (alias)   Pixel dimensions   DPC       DPI
======================= ================== ========= =========
 4320p (8k and uhd-2)    7680 x 4320       320        800
 2160p (4k and uhd)      3840 x 2160       160        400
 1080p (fhd and hd)      1920 x 1080       80         200
 720p                    1280 x 720        53.3333    133.333
 540p                    960 x 540         40         100
 480p                    854 x 480         35.5833    88.958
 360p                    640 x 360         26.6667    66.667
 240p                    426 x 240         17.75      44.375
======================= ================== ========= =========


You should compose your plots using the given canvas size, and movie will make proper conversions of the canvas to image pixel dimensions.

       .. image:: Canvas_16x9.png


- By default, the canvas has an offset of 2.54 cm (or 1 inch) in X and Y.

.. Note::
   There are also presets formats for 4:3 format (uxga, sxga+, xga, svga, dvd).


**Custom format**: 

- If you want another dimensions, you can just set a custom format.
- Tell -C both dimensions and the resolution (dpu).

2.2.2.5. Second attemp. Fix the canvas
++++++++++++++++++++++++++++++++++++++

* Set a custom canvas of a square of 13 cm and 80 dpu (same resolution as full hd).
* I use ``-X0`` and ``-Y0`` (in the main script) to remove the default offset.


     .. gmtplot::
        :height: 300 px

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx80 -T10 -M0,png -V -L+f14p,Helvetica-Bold,white -Gblack



2.3. Make draft animation
^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we are happy with the master frame, we recommend you make a very short and small movie so you don't have to wait very long to see the result.
This is advisable because creating an animation can be time-consuming and there may be errors when generating many images and when they are assembled:
to reduce the number of frames (-T).
to reduce the quality of the frames (-C).

.. Note::
  The conversion to a video is done with FFmpeg (or GraphicsMagick if we ask for a GIF). 

.. admonition:: **Step Goals**:

  - to see if the frames are changing as we expected.
  - to see if there is video file is created well.


We add the following arguments:

- Fmp4: to create a video (now it is possible to delete ``-M``).
- Zs: to remove the temporary files created in the movie-making process.


2.3.1. First attemp
+++++++++++++++++++

    .. code-block:: bash

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx30 -T10 -M0,png -V -Gblack -L+f14p,Helvetica-Bold,white -Zs -Fmp4


  ..  youtube:: hHmXSYpV0yw
    :align: center
    :height: 300px
    :aspect: 1:1

**Error**:

- The movie doesn't change. We must learn about varibles.


Eliminating the explicit loop over time
+++++++++++++++++++++++++++++++++++++++

REVISAR TEXTO: 
In an animation, the illusion of movement is created by a rapid succession of frames (at least ca. 12 fps) that minimally differ from each other. The key idea in movie is for the user to write a single script (called mainscript) that makes the main idea of the animation and it is used for all frames. To introduce variations in them (otherwise, the movie would be incredibly boring), we use specific frame variables (see Table 2) that will automatically be updated as different frames are built. 

* The movie module creates animations by executing a main frame script for each frame time, making one frame image per frame time.
* The main script uses special variables whose values change with frame number.

* In order to introduce changes in the frames we must use the movie parameters.

**Movie parameters**

Constant parameters: These variables are constants throughout the movie.

============== =================================================================
 Parameter                            Purpose or contents                      
============== =================================================================
 MOVIE_NFRAMES   Total number of frames in the movie (via movie -T)            
 MOVIE_WIDTH     Width of the movie canvas                                     
 MOVIE_HEIGHT    Height of the movie canvas                                    
 MOVIE_DPU       Dots (pixels) per unit used to convert to image (via movie -C)
 MOVIE_RATE      Number of frames displayed per second (via movie -D)          
============== =================================================================

Variable parameters: These variables are updated for each frame (k, w are column number 0, 1, …).

============== ==============================================
 Parameter                  Purpose or contents
============== ==============================================
 MOVIE_FRAME    Number of current frame being processed
 MOVIE_TAG      Formatted frame number (string)
 MOVIE_NAME     Prefix for current frame image
 MOVIE_COLk     Variable k from data column k, current row
 MOVIE_TEXT     The full trailing text for current row 
 MOVIE_WORDw    Word w from trailing text, current row 
============== ==============================================


2.3.2 Second attemp. Use variables
++++++++++++++++++++++++++++++++++

- I use the `MOVIE_FRAME` variable to set the central longitude of the map.
  This is a variable parameter, so it will change from 0 to 10.

- It is possible also to use the `MOVIE_WIDTH` parameter to set the widht of the map. 
  This is a constant parameter and it will remain fixed (to 13 cm) in all the frames.

      .. code-block:: bash

        cat << 'EOF' > main.sh
        gmt begin
         gmt grdimage @earth_relief_06m -I -JG-${MOVIE_FRAME}/0/${MOVIE_WIDTH} -Y0 -X0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx30 -T10 -M0,png -V -Gblack -L+f14p,Helvetica-Bold,white -Fmp4 -Zs

.. Note::
 
  I add a minus sign so the earth spinns in the correct sense.


..  youtube:: sagKzhI88tU
    :align: center
    :height: 300px
    :aspect: 1:1


2.4. Make full animation
^^^^^^^^^^^^^^^^^^^^^^^^
- Once that our simple animation is working you can increment the number of frames (-T) and movie quality (-C).
- I increase the amount of frames to 360 (``-T360``) 
- and increment the resolution to 80 dots per cm (``-C13cx13cx80``).

    .. code-block:: bash
     
        cat << 'EOF' > main.sh
        gmt begin
         gmt grdimage @earth_relief_06m -I -JG-${MOVIE_FRAME}/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx80 -T360 -M0,png -V -Gblack -L+f14p,Helvetica-Bold,white -Fmp4 -Zs

..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 300px
    :aspect: 1:1

.. Tip::

  Be carefull. This step could be quite time (and resources) consuming. 
  By default, `gmt movie` uses all the cores available to speed up the frame creation process.
  So probably you can't do anything else while GMT is creating all the frames (maybe you can take a break, or have lunch).


3. Tutorial 2. Earthquakes
~~~~~~~~~~~~~~~~~~~~~~~~~~

In this tutorial, I will explain a bit more complex type of animation.
This requires to use :gmt-module:`events` and :gmt-module:`movie` modules.
In this example, I will create an animation showing the occurrences of earthquakes during the year 2018: 

..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 300px
    :aspect: 1:1

This animation was done from 365 frames (one per day) which were shown at 24 frames per second (fps).


3.1. Goals of the Tutorial
==========================

- Explain the most important aspects of using the :gmt-module:`events` module.
- Explain more complex aspects of using the :gmt-module:`movie` module.

3.2. Step-by-step
=================

I will follow the same steps as described for tutorial 1.

3.2.1. Make last image
^^^^^^^^^^^^^^^^^^^^^^

In this example I will plot an static map of the earth. I create a cpt to plot the earthquakes.

     .. gmtplot::
        :height: 300 px

        gmt begin Earth png
            # Plot relief grid
            gmt grdimage @earth_relief_06m -I -JN14c
            # Create cpt for the earthquakes
            gmt makecpt -Cred,green,blue -T0,70,300,10000
            # Plot quakes
            gmt plot quakes.txt -SE- -C
        gmt end


3.2.2. Make master frame
^^^^^^^^^^^^^^^^^^^^^^^^

For this example, it is suggested to use a background script (pre.sh.) 
This is used for two purposes: 

#. (1) To create a cpt file that will be needed by mainscript to make the movie, 
#. (2) To make a static background plot that should form the background for all frames.

So, in this background script I create the CPT for the earthquakes and plot the background map. Note that I use a constant parameter (``${MOVIE_WIDTH}``).

I also include a label with the date (``-Lc0``).

     .. gmtplot::
        :height: 300 px
        
        cat << 'EOF' > pre.sh
        gmt begin
          # Create background map
          gmt grdimage @earth_relief_06m -I -JN${MOVIE_WIDTH} -Rg -X0 -Y0
          # Create cpt for the earthquakes
          gmt makecpt -Cred,green,blue -T0,70,300,10000 -H > quakes.cpt
        gmt end
        EOF

        cat << 'EOF' > main.sh
        gmt begin
          gmt basemap -Rg -JN${MOVIE_WIDTH} -X0 -Y0 -B+n
          gmt plot quakes.txt -SE- -Cquakes.cpt
          gmt events quakes.txt -SE- -Cquakes.cpt -T${MOVIE_COL0}
        gmt end
        EOF

        gmt movie main.sh -Sbpre.sh -NEarth -Ml,png -Zs -V -C720p \
        -T2018-01-01T/2018-12-31T/1d -Gblack \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


3.2.3. Make full animation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. code-block:: bash

        cat << 'EOF' > pre.sh
        gmt begin
          # Create background map
          gmt grdimage @earth_relief_06m -I -JN${MOVIE_WIDTH} -Rg -X0 -Y0
          # Create cpt for the earthquakes
          gmt makecpt -Cred,green,blue -T0,70,300,10000 -H > quakes.cpt
        gmt end
        EOF

        cat << 'EOF' > main.sh
        gmt begin
          gmt basemap -Rg -JN${MOVIE_WIDTH} -X0 -Y0 -B+n
          #gmt plot quakes.txt -SE- -Cquakes.cpt
          gmt events quakes.txt -SE- -Cquakes.cpt -T${MOVIE_COL0}
        gmt end
        EOF

        gmt movie main.sh -Sbpre.sh -NEarth -Ml,png -Zs -V -C24cx12cx80 \
        -T2018-01-01T/2018-12-31T/1d -Gblack -Fmp4 \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 300px
    :aspect: 2:1


3.2.4. Make full animation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the previous animation, the earthquakes appear. The module events include options that can modify and enhance the earthquakes.
The -E option allows to set the duration of the phases. 
The -M option modify the symbols during the phases:

-Es+r2+d6: This sets the duration of the rise phase and the decay phase. 
- Ms5+c0.5: modify the relative size of the symbol. The size increase 5 times and them reduce by half (of the original size) in the coda phase.
- Mt+c0: modify the transparency to 0 in the coda fade. This allows that the symbols continue to be seen after its occurrence. 
- Mi1+c-0.6: modify the intensity of the color. It gets lighter and then darker in the coda phase.




    .. code-block:: bash

        cat << 'EOF' > pre.sh
        gmt begin
          # Create background map
          gmt grdimage @earth_relief_06m -I -JN${MOVIE_WIDTH} -Rg -X0 -Y0
          # Create cpt for the earthquakes
          gmt makecpt -Cred,green,blue -T0,70,300,10000 -H > quakes.cpt
        gmt end
        EOF

        cat << 'EOF' > main.sh
        gmt begin
          gmt basemap -Rg -JN${MOVIE_WIDTH} -X0 -Y0 -B+n
          gmt events quakes.txt -SE- -Cquakes.cpt -T${MOVIE_COL0} \
          -Es+r2+d6 -Ms5+c0.5 -Mi1+c-0.6 -Mt+c0 --TIME_UNIT=d
        gmt end
        EOF

        gmt movie main.sh -Sbpre.sh -NEarth -Ml,png -Zs -V -C24cx12cx80 \
        -T2018-01-01T/2018-12-31T/1d -Gblack -Fmp4 \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 300px
    :aspect: 2:1


4. References
~~~~~~~~~~~~~

- Wessel, P., Esteban, F., & Delaviel-Anger, G. (2024). The Generic Mapping Tools and animations for the masses. 
Geochemistry, Geophysics, Geosystems, 25, e2024GC011545. https://doi.org/10.1029/2024GC011545.


Technical information:

- gmt movie: <https://docs.generic-mapping-tools.org/6.5/movie.html>


See also more animations examples:

- GMT animation gallery: https://docs.generic-mapping-tools.org/6.5/animations.html. 
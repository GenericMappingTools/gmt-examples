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

Corregir link

..  youtube:: NjSDpQ5S3FM
   :height: 80%


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
        gmt movie main.sh -NEarth -Cfhd -T10 -M0,png -Gblack -V


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
        gmt movie main.sh -NEarth -C13cx13cx80 -T10 -M0,png -Gblack -V


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

     #.. gmtplot::
        :height: 300 px

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx30 -T10 -M0,png -Gblack -V -Zs -Fmp4

Corregir link

..  youtube:: NjSDpQ5S3FM
   :height: 80%

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


     #.. gmtplot::
        :height: 300 px
  
        cat << 'EOF' > main.sh
        gmt begin
         gmt grdimage @earth_relief_06m -I -JG-${MOVIE_FRAME}/0/${MOVIE_WIDTH} -Y0 -X0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx30 -T10 -Mf,png -Gblack -V -Fmp4

.. Note::
 
  I add a minus sign so the earth spinns in the correct sense.


Corregir link

..  youtube:: NjSDpQ5S3FM
   :height: 80%


2.4. Make full animation
^^^^^^^^^^^^^^^^^^^^^^^^
- Once that our simple animation is working you can increment the number of frames (-T) and movie quality (-C).
- I increase the amount of frames to 360 (``-T360``) 
- and increment the resolution to 80 dots per cm (``-C13cx13cx80``).


     #.. gmtplot::
        :height: 300 px
      
        cat << 'EOF' > main.sh
        gmt begin
         gmt grdimage @earth_relief_06m -I -JG-${MOVIE_FRAME}/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -C13cx13cx80 -T360 -M0,png -NEarth -Gblack -V -Fmp4


Corregir link

..  youtube:: NjSDpQ5S3FM
   :height: 80%


.. Tip::

  Be carefull. This step could be quite time (and resources) consuming. 
  By default, `gmt movie` uses all the cores available to speed up the frame creation process.
  So probably you can't do anything else while GMT is creating all the frames (maybe you can take a break, or have lunch).


3. Tutorial 2. Earthquakes
~~~~~~~~~~~~~~~~~~~~~~~~~~



4. References
~~~~~~~~~~~~~

* Wessel, P., Esteban, F., & Delaviel-Anger, G. (2024). The Generic Mapping Tools and animations for the masses. 
Geochemistry, Geophysics, Geosystems, 25, e2024GC011545. https://doi.org/10.1029/2024GC011545.

Technical information:

* gmt movie: <https://docs.generic-mapping-tools.org/6.5/movie.html>

See also more animations examples:

* GMT animation gallery: https://docs.generic-mapping-tools.org/6.5/animations.html. 
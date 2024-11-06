Making animations
-----------------

By F. Esteban (@esteban82). November, 2024


- This tutorial explain the basic aspect of doing animations with GMT.
- It serve as a guide to help beginners understand and troubleshoot potential issues.
- It explain basic aspect of the :gmt-module:`movie` and :gmt-module:`events` modules.


1. Introduction
~~~~~~~~~~~~~~~

Prior to GMT 6.0, ambitious movie makers would have to write complicated scripts where the advancement of frames was explicitly done by a shell loop, 
and then perhaps that frame counter was used to make some changes to other parameters so that when the plotting started the plot would differ from the previous one. 
At the end of the script, you would have to convert your PostScript plot to a raster image with a name that is lexically increasing, 
and then later you would use some external software to assemble the movie. Hence, only very brave GMT users attempted to make GMT animations. 
Here you can see a `more complete explanation <https://docs.generic-mapping-tools.org/5.4/gallery/anim_introduction.html>`_ 
and `some examples <https://docs.generic-mapping-tools.org/5.4/Gallery.html#animations>`_ of that times.

GMT 6 (`Wessel et al 2019 <https://doi.org/10.1029/2019GC008515>`_) simplified all that by adding movie-making modules
that were later refined with GMT 6.5 (`Wessel et al 2024 <https://doi.org/10.1029/2024GC011545>`_). 
These modules empower users to create animations by taking over non-trivial tasks.

1.1 What is an Animation?
=========================

- Animation is a technique used to create the illusion of motion.
- This is achieved by displaying a rapid sequence of still images (at least 12 frames per second).


1.2. How to Make an Animation
=============================

In order to make an animation we need:

#. A series of still images.
#. A method to combine these images into a video format.

.. admonition:: Technical Information
  A video file is essentially a container format that sequentially displays all the images it contains.


1.3. Why use GMT for animations?
================================

GMT is ideal for animations that require:

- Scientific precision.
- Handling geospatial data.
- High-quality graphical visualizations.

1.4. Types of animations in GMT
================================

In GMT, animations can generally be categorized by their complexity:

#. **Moving objects** (e.g., Earth spinning), created using the :gmt-module:`movie` module.
#. **Appearing Objects** (e.g., earthquakes), created using both the :gmt-module:`movie` and :gmt-module:`events` modules.


1.5. Prerequisites
==================

- GMT version 6.5 or later.


2. Tutorial 1. Earth spinning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this part of the tutorial, I will explain the simplest type of animation, 
which only requires :gmt-module:`movie` module. 

As an example, I will create an animation of the Earth spinning similar to the one below.

..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 400px
    :aspect: 1:1


.. admonition:: Technical Information

  This animation was created from 360 images (or frames), each frame rotating by 1 degree in the central longitude of the map, 
  and is displayed at 24 frames per second (fps).

2.1. Goals of the Tutorial
==========================

- Explain the most important aspects of using the :gmt-module:`movie` module which include:

  - What is GMT movie
  - How to set the Canvas (-C)
  - How to set the movie parameters


2.2. Step-by-step Instructions
==============================

To create an animation, follow these steps:

#. Make first image
#. Make master frame with gmt movie
#. Make draft animation
#. Make full animation

2.2.1. Make first image
^^^^^^^^^^^^^^^^^^^^^^^

The first step is to create an image using a standard GMT script 
(with `modern mode <https://docs.generic-mapping-tools.org/dev/reference/introduction.html#modern-and-classic-mode>`_) 
that will serve as the base for the animation.

**Step Goal**: Create the first image of the animation.

For this example, I create a map of the Earth with:

     .. gmtplot::
        :height: 400 px

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

To create animations with GMT, we use the :gmt-module:`movie` module. 
In this step, I use it to recreate the previous image (the *master frame*).

.. Important::

  **Step Goal**: Make a master frame that looks identical to the first image.

2.2.2.1. What is GMT movie?
++++++++++++++++++++++++++++

The :gmt-module:`movie` module simplifies most of the steps needed to create an animation 
by executing a single plot script that is repeated across all frames.

**Required Arguments:**

- **mainscript**: The previously created script.
- **-N**: Name for the output file.
- **-C**: Canvas Size.
- **-T**: Number of frames.
- There are two type of outputs. An image (called *master frame*; **-M**) or a video (**-F**). You have to asks for at least one of them.

**Optional Arguments** (useful for this tutorial):

- **-G**: Set the canvas color (or fill).
- **-V**: Show verbose information during the movie-making process.
- **-L**: Show a label with the frame number. 

2.2.2.2. First Attempt
++++++++++++++++++++++

I create the first frame (``-M0,png``) over a black canvas (``-G``) for an HD video format (``-Chd``).

     .. gmtplot::
        :height: 400 px

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c
        gmt end
        EOF
        gmt movie main.sh -NEarth -Chd -T360 -M0,png -V -L+f14p,Helvetica-Bold,white -Gblack


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
  - This is useful because allow us to see (and edit) the main script and the arguments of gmt-module:`movie` just using a single file.


2.2.2.3. Fix the Canvas
+++++++++++++++++++++++

**What is the Canvas?**

- The canvas is the black area of the previous image.
- This is the working area of the frames. 
- The elements of the main script must be drawn inside the canvas.
- The elements that are outside will not (totally or partially) appear in the animation.
- The canvas size is important by two reasons:

  - to set the final dimension in pixels of the frames/movie (i.e. the quality).
  - set the width and height (in cm or inches) of the frames.

**How to set the canvas**:

- This is set via ``movie -C``.
- There are two ways to the set the canvas:

  - Presets format
  - Custom format

**Presets format**:

- It is the easiest way to specify the canvas.
- Use the name (or alias) to select a format based on this table (for 16:9 format):

 ======================= ================== =========
  Preset format (alias)   Pixel dimensions   DPC     
 ======================= ================== =========
  4320p (8k and uhd-2)    7680 x 4320       320      
  2160p (4k and uhd)      3840 x 2160       160      
  1080p (fhd and hd)      1920 x 1080       80       
  720p                    1280 x 720        53.3333  
  540p                    960 x 540         40       
  480p                    854 x 480         35.5833  
  360p                    640 x 360         26.6667  
  240p                    426 x 240         17.75    
 ======================= ================== =========

- Pixel density (dots-per-cm, dpc) is set automatically. 
- For the 16:9 format, the canvas is 24 x 13.5 cm: 


     .. gmtplot::
        :height: 400 px
        :align: center
        :show-code: FALSE

        gmt begin Canvas png
          gmt basemap -Jx0.5c -R0/24/0/13.5 -B+glightgreen+t"16x9 format" --FONT_TITLE=24,Helvetica
          gmt basemap -Ba5f1g5+u" cm" -BWeSn
	        echo 24 cm by 13.5 cm | gmt text -F+f24p+cMC -Gwhite
        gmt end


.. Important::

  - By default, the canvas has an offset of 2.54 cm (or 1 inch) in X and Y.

.. Note::

   - You can also specify the dimensions in inches (or points).
   - There are also presets formats for 4:3 (uxga, sxga+, xga, svga, dvd).


**Custom format**:

- If you want another dimensions, you can request a custom format directly by giving width and height (in cm or inches) and dpu (*widthxheightxdpu*).


.. Important::

  - DPU: Dots-per-unit pixel density. So it is DPI for inches or DPC for cm. 


2.2.2.5. Second attempt. Fix the canvas
++++++++++++++++++++++++++++++++++++++

- For this new attempt I will:

  - set a custom canvas of a square of 13 cm and 80 dpu (same resolution as full hd, ``-C13cx13cx80``).
  - use ``-X0`` and ``-Y0`` (in ``main.sh``) to remove the default offset.


     .. gmtplot::
        :height: 400 px

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx80 -T360 -M0,png -V -L+f14p,Helvetica-Bold,white -Gblack


2.3. Make draft animation
^^^^^^^^^^^^^^^^^^^^^^^^^

Once you are happy with the master frame, I recommend to make a very short and small movie so you don't have to wait very long to see the result.
This approach is advisable because creating an animation can be time-consuming, 
and generating many images for assembly can sometimes lead to errors or unexpected behaviors.

.. admonition:: **Step Goals**:

  - to see if the frames are changing as expected.
  - to see if the video file is created properly.


.. Note::

  The conversion to a video format relies on `FFmpeg <https://www.ffmpeg.org/>`_ (for MP4 or WebM) 
  and `GraphicsMagick <http://www.graphicsmagick.org/>`_ (for GIF).


2.3.1. First attempt
++++++++++++++++++++

In this example I will reduce the number of frames to 10 (``-T10``) and the quality to 30 DPC (``-C13cx13cx30``).
Also, I add the following arguments to :gmt-module:`movie`:

- Fmp4: to create a mp4 video (now it is possible to delete ``-M``).
- Zs: to remove the temporary files created in the movie-making process. Useful to keep the working directory clean.


    .. code-block:: bash

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx30 -T10 -M0,png -V -Gblack -L+f14p,Helvetica-Bold,white -Fmp4 -Zs


  ..  youtube:: hHmXSYpV0yw
    :align: center
    :height: 400px
    :aspect: 1:1


.. Error::

  - The movie doesn't change. We must learn about parameters.

Movie Parameters
++++++++++++++++

The key idea in :gmt-module:`movie` is for the user to write the main script that makes the idea of the animation and it is used for all frames.
To introduce variations in the frames (otherwise, the movie would be incredibly boring), 
we must use variables parameters that will automatically be updated as different frames are built. 
Several parameters are automatically assigned (via the movie module) and can be used when composing the main script.

- There are two sets of parameters:

  - Variable
  - Constant 

**Variable parameters**: Whose values change with the frame number.

 ============== ============================================= ===============
  Parameter                  Purpose or contents               Set by Movie
 ============== ============================================= ===============
  MOVIE_FRAME    Number of current frame being processed       -T
  MOVIE_TAG      Formatted frame number (string)               -T 
  MOVIE_NAME     Prefix for current frame image                -N and -T
  MOVIE_COLk     Variable k from data column k, current row    -T\ *timefile*
  MOVIE_TEXT     The full trailing text for current row        -T\ *timefile*
  MOVIE_WORDw    Word w from trailing text, current row        -T\ *timefile*
 ============== ============================================= ===============


**Constant parameters**: Whose values do NOT change during the whole movie.
 
 ============== ================================================= =============
  Parameter               Purpose or contents                       Set by 
 ============== ================================================= =============
  MOVIE_NFRAMES   Total number of frames in the movie               movie -T
  MOVIE_WIDTH     Width of the movie canvas                         movie -C
  MOVIE_HEIGHT    Height of the movie canvas                        movie -C
  MOVIE_DPU       Dots (pixels) per unit used to convert to image   movie -C
  MOVIE_RATE      Number of frames displayed per second             movie -D 
 ============== ================================================= =============

.. Important::
    
    - In order to introduce changes in the frames we must use the movie variable parameters.

How to set the number of Frames
+++++++++++++++++++++++++++++++

There are 3 ways to set the number of frames for a movie:

**1. Number**: 

If you write a single (integer) value, them it will be the total number of frames. 
Under the hood, this will create a one-column data set from 0 to that number every 1 value. 
In this case, you can use MOVIE_FRAME to get that value for each frame.

**2. min/max/inc**:

If you write 3 values, then GMT will create a one-column data set from *min* to *max* every *inc*.
In this case the total of number will be total amount of rows that the one-column data set will have.
In this case, you case also use the MOVIE_COL0 parameter to access the first column of the data set.

**3. Time file**:

If you supply the name of a file, then GMT will access it and use one record (i.e. row) per frame.
This method allow to have more than one-column and can be used to make more complex animations. 
For example, you can have a second column with numbers which will access with MOVIE_COL1.
The file can even have trailing text that will be accessed with MOVIE_TEXT.


2.3.2 Second attempt. Use parameters
++++++++++++++++++++++++++++++++++++

Now I will update the script with movie parameters. 
First, I use ``MOVIE_FRAME`` variable parameter to set the central longitude of the map.
Since I using ``-T10``, I will get an animation with 10 frames, where the longitude will range from 0 to 9. 
I also use the ``MOVIE_WIDTH`` constant parameter to set the width of the map (instead of 13c).

      .. code-block:: bash

        cat << 'EOF' > main.sh
        gmt begin
         gmt grdimage @earth_relief_06m -I -JG-${MOVIE_FRAME}/0/${MOVIE_WIDTH} -Y0 -X0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx30 -T10 -M0,png -V -Gblack -L+f14p,Helvetica-Bold,white -Fmp4 -Zs

.. Note::
 
  I add a minus sign so the earth spins in the correct sense.


..  youtube:: sagKzhI88tU
    :align: center
    :height: 400px
    :aspect: 1:1


2.4. Make full animation
^^^^^^^^^^^^^^^^^^^^^^^^
Once that the draft animation is working it is possible to increment the number of frames (-T) and movie quality (-C).

In the example, I increase:

- the amount of frames to 360 (``-T360``) to get the whole spin.
- the resolution to 80 DPC (``-C13cx13cx80``) to get a high-quality video.

    .. code-block:: bash
     
        cat << 'EOF' > main.sh
        gmt begin
         gmt grdimage @earth_relief_06m -I -JG-${MOVIE_FRAME}/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx80 -T360 -M0,png -V -Gblack -L+f14p,Helvetica-Bold,white -Fmp4 -Zs

..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 400px
    :aspect: 1:1

.. Tip::

  Be careful. This step can be quite time (and resource) consuming.
  By default, :gmt-module:`movie` uses all the cores available to speed up the frame creation process.
  So probably you can't do anything else while GMT is creating all the frames (maybe you can take a break, or have lunch).


3. Tutorial 2. Earthquakes
~~~~~~~~~~~~~~~~~~~~~~~~~~

In this tutorial, I will explain a bit more complex type of animation.
This requires to use :gmt-module:`events` and :gmt-module:`movie` modules.
In this example, I will create an animation showing the occurrences of earthquakes during the year 2018: 

..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 400px
    :aspect: 1:1

This animation was done from 365 frames (one per day) which were shown at 24 frames per second (fps).


3.1. Goals of the Tutorial
==========================

- Explain the most important aspects of using the :gmt-module:`events` module.
- Explain more complex aspects of using the :gmt-module:`movie` module.

3.2. Step-by-step
=================

I will follow the same steps as described for tutorial 1 (except for the draft animation).

3.2.1. Make last image
^^^^^^^^^^^^^^^^^^^^^^

In this example I will plot an static map of the earth. I create a cpt to plot the earthquakes.

     .. gmtplot::
        :height: 400 px

        gmt begin Earth png
            # Plot relief grid
            gmt grdimage @earth_relief_06m -I -JN14c
            # Create cpt for the earthquakes
            gmt makecpt -Cred,green,blue -T0,70,300,10000
            # Plot quakes
            gmt plot @quakes_2018.txt -SE- -C
        gmt end

.. admonition:: Technical Information

    - I used the earthquakes from the file `quakes_2018.txt <https://github.com/GenericMappingTools/gmtserver-admin/blob/master/cache/quakes_2018.txt>`_ which has 5 columns.

     ============== ========== ======== ================ ======================== 
      Longitude      Latitude   Depth    Magnitude (x50)          Date           
     ============== ========== ======== ================ ======================== 
      46.4223        -38.9126     10        260           2018-01-02T02:16:18.11  
      169.3488       -18.8355   242.77      260           2018-01-02T08:10:00.06  
      ...                                                                
     ============== ========== ======== ================ ========================
    - The same file was used for animation 08. Check it to see how it was download and process.


3.2.2. Make master frame
^^^^^^^^^^^^^^^^^^^^^^^^

The background script
+++++++++++++++++++++

Within movie, there is an optional background script that it is used for two purposes:

#. Create files that will be needed by main script to make the movie, 
#. Make a static background plot that should form the background for all frames 



For this example, I use the background script (pre.sh.) to: 

#. To create a cpt file that will be used to color the quakes.
#. To make a worldwide background map.

So, in this background script I create the CPT for the earthquakes and plot the background map. Note that I use a constant parameter (``${MOVIE_WIDTH}``).

For the main script, I use events (instead of plot). In order to use it, I only add the parameter ``-T`` which indicate the *time* of the events.
I also include a label with the date (``-Lc0``).

     .. gmtplot::
        :height: 400 px
        
        cat << 'EOF' > pre.sh
        gmt begin
          # Set parameters and position
          gmt basemap -Rg -JN${MOVIE_WIDTH} -X0 -Y0 -B+n
          # Create background map
          gmt grdimage @earth_relief_06m -I
          # Create cpt for the earthquakes
          gmt makecpt -Cred,green,blue -T0,70,300,10000 -H > quakes.cpt
        gmt end
        EOF

        cat << 'EOF' > main.sh
        gmt begin
          gmt basemap -Rg -JN${MOVIE_WIDTH} -X0 -Y0 -B+n
          #gmt plot @quakes_2018.txt -SE- -Cquakes.cpt
          gmt events @quakes_2018.txt -SE- -Cquakes.cpt -T${MOVIE_COL0}
        gmt end
        EOF

        gmt movie main.sh -Sbpre.sh -NEarth -Ml,png -Zs -V -C720p \
        -T2018-01-01T/2018-12-31T/1d -Gblack \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-

.. admonition:: Technical Information

  - **--FONT_TAG=18p,Helvetica,white**: This set the font for the label.
  - **--FORMAT_CLOCK_MAP=-**: This works to NOT include the hours in the date.


3.2.3. Make full animation without enhancement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, I will make the final animation. In this example, the command executed in the main script is simple so you can avoid making a draft animation.

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
          gmt events @quakes_2018.txt -SE- -Cquakes.cpt -T${MOVIE_COL0}
        gmt end
        EOF

        gmt movie main.sh -Sbpre.sh -NEarth -Ml,png -Zs -V -C24cx12cx80 \
        -T2018-01-01T/2018-12-31T/1d -Gblack -Fmp4 \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


..  youtube:: dbOjYqWzGi0
    :align: center
    :height: 400px
    :aspect: 2:1


3.2.4. Make full animation with enhancement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the previous animation, the earthquakes appear but it is hard to see when they do it. 
With :gmt-module:`events` is possible to draw attention to the arrival of a new event by temporarily changing four attributes of the symbol (via -M): 
 
- Size
- Color intensity 
- Transparency 
- Color (via CPT look-up).

The duration of the temporary changes are control via the -E modifier.


In this example I announce each quake by magnifying size and whitening the color for a little bit. Later the symbols return to its original properties.

.. admonition:: Technical Information

  - \--TIME_UNIT=d: This sets that the values of -E are in days (d).
  - -Es+r2+d6: This sets the duration of the rise phase and the decay phase.
  - -Ms5+c1: modify the size. The size will increase 5 times during the rise phase and them reduce to the original size.
  - -Mt+c0: modify the transparency. The transparency will remain to 0 at the end. This allows to be seen after its occurrence. 
  - -Mi1+c0: modify the intensity of the color. It gets lighter during the rise phase and them returns to its original color.


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
          gmt events @quakes_2018.txt -SE- -Cquakes.cpt -T${MOVIE_COL0} \
          -Es+r2+d6 -Ms5+c1 -Mi1+c0 -Mt+c0 --TIME_UNIT=d
        gmt end
        EOF

        gmt movie main.sh -Sbpre.sh -NEarth -Ml,png -Zs -V -C24cx12cx80 \
        -T2018-01-01T/2018-12-31T/1d -Gblack -Fmp4 \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


..  youtube:: rmPhIVzhIgY
    :align: center
    :height: 400px
    :aspect: 2:1


4. See also
~~~~~~~~~~~

The paper about animations which include explanation and examples (Wessel 2024).

Check the modules documentation for full technical information:

- :gmt-module:`movie`
- :gmt-module:`events`

You can find more examples here:

- GMT animation gallery: https://docs.generic-mapping-tools.org/6.5/animations.html. 

5. References
~~~~~~~~~~~~~

- Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F., & Tian, D. (2019). The Generic Mapping Tools Version 6. Geochemistry, Geophysics, Geosystems, 20(11), 5556–5564. https://doi.org/10.1029/2019GC008515
- Wessel, P., Esteban, F., & Delaviel-Anger, G. (2024). The Generic Mapping Tools and animations for the masses. Geochemistry, Geophysics, Geosystems, 25, e2024GC011545. https://doi.org/10.1029/2024GC011545.
Making animations
-----------------

By F. Esteban (@esteban82). November, 2024


- This tutorial explains the basic aspect of doing animations with GMT.
- It serves as a guide to help beginners understand and troubleshoot potential issues.
- It explains the basic aspect of the :gmt-module:`movie` and :gmt-module:`events` modules.


1. Introduction
~~~~~~~~~~~~~~~

Prior to GMT 6.0, ambitious movie makers had to write complicated scripts where the advancement of frames was explicitly done by a shell loop.
At the end of the script, you would have to convert your PostScript plot to a raster image with a name that is lexically increasing, 
and then later you would use some external software to assemble the movie. Hence, only very brave GMT users attempted to make GMT animations. 
Here you can see a `more complete explanation <https://docs.generic-mapping-tools.org/5.4/gallery/anim_introduction.html>`_ 
and `some examples <https://docs.generic-mapping-tools.org/5.4/Gallery.html#animations>`_ of those times.

GMT 6 (`Wessel et al. 2019 <https://doi.org/10.1029/2019GC008515>`_) simplified all that by adding movie-making modules
that were later refined with GMT 6.5 (`Wessel et al. 2024 <https://doi.org/10.1029/2024GC011545>`_). 
These modules empower users to create animations by taking over non-trivial tasks.


1.1. What is an Animation?
==========================

- Animation is a technique used to create the illusion of motion.
- This is achieved by displaying a rapid sequence of still images (at least 12 frames per second; fps).


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

For the purposes of this tutorial, I define two types of animations that can be made based on their complexity:

#. **Moving object** (e.g., Earth spinning), created using the :gmt-module:`movie` module.
#. **Appearing object** (e.g., earthquakes), created using both the :gmt-module:`movie` and :gmt-module:`events` modules.


1.5. Prerequisites
==================

- GMT version 6.5 or later.


2. Tutorial 1. Earth spinning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here I explain how to make an animation of a moving object which only requires the :gmt-module:`movie` module. 

As an example, I will create an animation of the Earth spinning like the one below.

..  youtube:: uZtyTv6DLnM
    :align: center
    :height: 400px
    :aspect: 1:1


.. admonition:: Technical Information

  This animation was created using 360 images (or frames), with each frame representing a 1-degree rotation in the central longitude of the map, 
  displayed at 24 fps.


To create the animation, I follow these four steps:

#. Make first image
#. Make master frame with gmt movie
#. Make draft animation
#. Make full animation


2.1. Goals of the Tutorial
==========================

- Explain the most important aspects of using the :gmt-module:`movie` module which include:

  - What is :gmt-module:`movie`
  - How to set the Canvas (-C)
  - What are and how to use the movie parameters
  - How to set the number of Frames (-T)


2.2. Make first image
======================

The first step is to create an image using a standard GMT script 
(with `modern mode <https://docs.generic-mapping-tools.org/dev/reference/introduction.html#modern-and-classic-mode>`_) 
that will serve as the base for the animation.

.. Important::

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
  - **-JG0/0/13c**: Perspective projection with the center at longitude 0 and latitude 0, with a 13 cm map width.


2.3. Make the Master Frame
===========================

In this second step, I recreate the previous image but with the :gmt-module:`movie` module which is used to create animations. 


.. Important::

  **Step Goal**: Make a master frame that looks identical to the first image.

2.3.1. What is GMT movie?
^^^^^^^^^^^^^^^^^^^^^^^^^

The :gmt-module:`movie` module simplifies most of the steps needed to create an animation 
by executing a single plot script that is repeated across all frames.

**Required Arguments:**

- **mainscript**: Script that will be used to create all the frames.
- **-N**: Name for the output file.
- **-C**: Canvas Size (see below).
- **-T**: Number of frames (see below).
- There are two types of outputs. An image (called *master frame*; **-M**) or a video (**-F**). You have to ask for at least one of them.

**Optional Arguments** (useful for this tutorial):

- **-G**: Set the canvas color (or fill).
- **-V**: Show verbose information during the movie-making process.
- **-L**: Show a label with the frame number. 

2.3.2. First Attempt
^^^^^^^^^^^^^^^^^^^^^

In the first attempt, I create the first frame (``-M0,png``) over a black canvas (``-Gblack``) for an HD video format (``-Chd``).

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

  - The previous script is enclosed between ``cat << 'EOF' > main.sh`` and ``EOF``.
  - This creates the ``main.sh`` file on-the-fly (using a `Here Document <https://en.wikipedia.org/wiki/Here_document>`_).
  - This is useful because it allows us to see (and edit) the main script and the arguments of :gmt-module:`movie` just using a single file.


2.3.3. The Canvas
^^^^^^^^^^^^^^^^^^^

**What is the Canvas?**

- The canvas is the black area of the previous image.
- This is the working area of the frames. 
- The elements of the main script must be drawn inside the canvas.
- The elements that are outside will be (totally or partially) hidden in the animation.
- The canvas size is important by two reasons:

  - to set the width and height (in cm or inches) of the frames.
  - to set the dimensions in pixels of the frames/movie (i.e. the quality).
  

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
   - There are also preset formats for 4:3 (uxga, sxga+, xga, svga, dvd).


**Custom format**:

- If you want another dimension, you can request a custom format directly by giving width and height and dpu (*widthxheightxdpu*).


.. Important::

  - DPU: Dots-per-unit pixel density. So, it is DPI for inches or DPC for centimeters.


2.3.4. Second attempt. Fix the canvas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For this new attempt I:

  - use a custom canvas of a square of 13 cm and 80 dpc (same resolution as full hd, ``-C13cx13cx80``).
  - use ``-X0`` and ``-Y0`` (in ``main.sh``) to remove the default offset.


     .. gmtplot::
        :height: 400 px

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx80 -T360 -M0,png -V -L+f14p,Helvetica-Bold,white -Gblack


2.4. Make draft animation
=========================

Once the master frame is ok, I recommend making a very short and small movie so you don't have to wait very long to see the result.

.. admonition:: **Step Goals**:

  - See that the video file is created properly.
  - See that the frames are changing as expected.


.. Note::

  The conversion to a video format relies on `FFmpeg <https://www.ffmpeg.org/>`_ (for MP4 or WebM) 
  and `GraphicsMagick <http://www.graphicsmagick.org/>`_ (for GIF).


2.4.1. First attempt
^^^^^^^^^^^^^^^^^^^^^^

In this step I reduce the number of frames to 10 (``-T10``) and the quality to 30 DPC (``-C13cx13cx30``).
Also, I add the following arguments to :gmt-module:`movie`:

- **-Fmp4**: to create a mp4 video (now it is possible to delete ``-M``).
- **-Zs**: to remove the temporary files created in the movie-making process. Useful to keep the working directory clean.


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

.. Note::

  The display frame rate is set by default to 24 `fps <https://en.wikipedia.org/wiki/Frame_rate>`_. It can be change with `-D <https://docs.generic-mapping-tools.org/dev/movie.html#d>`_.


.. Error::

  - The movie doesn't change. We must learn about parameters.

2.4.2. Movie Parameters
^^^^^^^^^^^^^^^^^^^^^^^^

The movie parameters are key to making animations.
They are automatically assigned by different movie arguments (see tables below). 
There are two sets of parameters:

.. The key idea in :gmt-module:`movie` is for the user to write the main script that makes the idea of the animation and it is used for all frames.

**Variable parameters**: 

- These values change with the frame number.
- They must be used in the *main script* to introduce variations in the frames.


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


**Constant parameters**:

- These values do NOT change during the whole movie.
- They can be used in the *main script* (and in the optional background and foreground scripts).


 ============== ================================================= =====================
  Parameter               Purpose or contents                      Set by Movie
 ============== ================================================= =====================
  MOVIE_NFRAMES   Total number of frames in the movie               -T
  MOVIE_WIDTH     Width of the movie canvas                         -C
  MOVIE_HEIGHT    Height of the movie canvas                        -C
  MOVIE_DPU       Dots (pixels) per unit used to convert to image   -C
  MOVIE_RATE      Number of frames displayed per second             -D
 ============== ================================================= =====================

.. Important::
    
    - In order to introduce changes in the frames we must use the **variable parameters**.

2.4.3. How to set the number of Frames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The number of frames (``-T``) is another important aspect to make animations.
There are 3 ways to do it:


1. **-TNumber**: 

If you supply a single (integer) value, then it will be the total number of frames. 
Under the hood, this will create a one-column data set from 0 to that number minus one.
For example, for ``-T10`` I get values from 0 to 9.
In the main script, you have to use the MOVIE_FRAME parameter to access the values.


2. **-Tmin/max/inc**:

If you supply 3 values, then GMT will create a one-column data set from *min* to *max*, incrementing by *inc*.
You have to use the MOVIE_COL0 parameter to access the values of the one-column data set.
The total of number of frames will be:

.. math::

     \text{total frames} = \frac{\text{max} - \text{min}}{\text{inc}} + 1


3. **-Ttimefile**:

If you supply the name of a file, then GMT will access it and use one record (i.e. row) per frame.
This method allows you to have more than one-column and can be used to make more complex animations. 
For example, you can have a second column with numbers that you can access using MOVIE_COL1.
The file can even have trailing text that will be accessed with MOVIE_TEXT.


2.4.4. Second attempt. Use parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now I update the script with movie parameters. 
First, I use the ``MOVIE_FRAME`` variable parameter to set the central longitude of the map.
I also use the ``MOVIE_WIDTH`` constant parameter (in ``main.sh``) to set the width of the map (instead of 13c).


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


2.5. Make full animation
=========================

Once the draft animation is working it is possible to increment the number of frames (-T) and movie quality (-C).

In the step, I increase:

- the number of frames to 360 (``-T360``) to get the whole spin.
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
  Also you could use `-x <https://docs.generic-mapping-tools.org/dev/gmt.html#core-full>`_ to specify the number of active cores to be used.


3. Tutorial 2. Earthquakes
~~~~~~~~~~~~~~~~~~~~~~~~~~

Here I explain how to make an animation with appearing objects. 
This is more complex and requires the use :gmt-module:`events` and :gmt-module:`movie` modules.
In this example, I create an animation showing the occurrences of earthquakes during the year 2018 (with one frame per day).
Note that the earthquakes are drawn as they occur and remain visible until the end of the animation.

.. ..  youtube:: rmPhIVzhIgY
..  youtube:: dbOjYqWzGi0
    :align: center
    :height: 400px
    :aspect: 2:1


.. |

For this tutorial I follow these steps:

#. Make image
#. Make master frame
#. Make draft animation
#. Make animation without enhancement
#. Make animation with enhancement


3.1. Goals of the Tutorial
==========================

- What is gmt :gmt-module:`events`.
- How to use a background script for a movie.
- How to enhance symbols with :gmt-module:`events`.


3.2 Make image
===============

In this step I plot a map of the earth with all the quakes from 2018.

     .. gmtplot::
        :height: 400 px

        gmt begin Earth png
            # Set parameters and position
            gmt basemap -Rg -JN14c -B+n
            # Plot relief grid
            gmt grdimage @earth_relief_06m -I
            # Create cpt for the earthquakes
            gmt makecpt -Cred,green,blue -T0,70,300,10000
            # Plot quakes
            gmt plot @quakes_2018.txt -SE- -C
        gmt end

.. admonition:: Technical Information

    - I use :gmt-module:`makecpt` to create a `CPT <https://docs.generic-mapping-tools.org/dev/reference/cpts.html#of-colors-and-color-legends>`_ to color the earthquakes.
    - I used the earthquakes from the file `quakes_2018.txt <https://github.com/GenericMappingTools/gmtserver-admin/blob/master/cache/quakes_2018.txt>`_ which has 5 columns.

     ============== ========== ======== ================ ========================
      Longitude      Latitude   Depth    Magnitude (x50)          Date
     ============== ========== ======== ================ ========================
      46.4223        -38.9126     10        260           2018-01-02T02:16:18.11
      169.3488       -18.8355   242.77      260           2018-01-02T08:10:00.06
      ...                                                 
     ============== ========== ======== ================ ========================
    - Note that the input file has the columns sorted as will be required by the :gmt-module:`plot` and :gmt-module:`events` modules. It was also used for `animation 08 <https://docs.generic-mapping-tools.org/dev//animations/anim08.html>`_. 
    Check it to see how it was downloaded and processed.


3.3. Make master frame
=======================

In this step I create the master frame of the animation similar to the previous image. 


3.3.1. First attempt (first frame)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this first attempt I create the first frame (``-Mf,png``) of the animation.


     .. gmtplot::
        :height: 400 px

        cat << 'EOF' > main.sh
        gmt begin
          # Set parameters and position
          gmt basemap -Rg -JN${MOVIE_WIDTH} -B+n -X0 -Y0
          # Create background map
          gmt grdimage @earth_relief_06m -I
          # Create cpt for the earthquakes
          gmt makecpt -Cred,green,blue -T0,70,300,10000
          gmt plot @quakes_2018.txt -SE- -C
        gmt end
        EOF

        gmt movie main.sh -NQuakes -Mf,png -Zs -V -C24cx12cx80 -T2018-01-01T/2018-12-31T/1d -Gblack \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


.. admonition:: Technical Information

  - I use ``-T2018-01-01T/2018-12-31T/1d`` to create a one-column data set with all days in 2018.
  - I use ``-Lc0`` to add a label with the first column (i.e. the dates).
  - **--FONT_TAG=18p,Helvetica,white**: This sets the font for the label.
  - **--FORMAT_CLOCK_MAP=-**: to NOT include the hours in the date and only plot year, month and day in the label.
  - I use a custom canvas of 24 x 12 cm with a resolution of 80 DPC (``-C24cx12cx80``).


.. Error::

  - The first frame contains all the quakes when none of them should be plotted. I must use :gmt-module:`events` instead.


3.3.2. The events module
^^^^^^^^^^^^^^^^^^^^^^^^

In the previous figure, I use the :gmt-module:`plot` module to draw the symbols. This results that the symbols appear on all frames.
However if I want to plot quakes as they unfold, I have to use the :gmt-module:`events` instead. 


.. Important::

  - :gmt-module:`events` requires a time column in the input data and will use it and the animation time to determine when symbols should be plotted.
  - The ``-T`` is a required argument and is used to set the current plot time.


3.3.3. Second attempt (first frame with events)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Now, in this attempt I use :gmt-module:`events`. I use with ``-T${MOVIE_COL0}`` to plot the quakes as dates progresses


     .. gmtplot::
        :height: 400 px

        cat << 'EOF' > main.sh
        gmt begin
          # Set parameters and position
          gmt basemap -Rg -JN${MOVIE_WIDTH} -B+n -X0 -Y0
          # Create background map
          gmt grdimage @earth_relief_06m -I
          # Create cpt for the earthquakes
          gmt makecpt -Cred,green,blue -T0,70,300,10000
          gmt events @quakes_2018.txt -SE- -C -T${MOVIE_COL0}
        gmt end
        EOF

        gmt movie main.sh -NQuakes -Mf,png -Zs -V -C24cx12cx80 -T2018-01-01T/2018-12-31T/1d -Gblack \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


.. Warning::
  The map shows NO earthquakes. This is expected because there are no quakes (in the data file) before January first.
  However, this could also be due to an error in the command.
  I must plot the frame from another date to see if the quakes appear.


3.3.4. Third attempt (last frame with events)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, I also plot the last frame (``-Ml``). 

     .. gmtplot::
        :height: 400 px

        cat << 'EOF' > main.sh
        gmt begin
          # Set parameters and position
          gmt basemap -Rg -JN${MOVIE_WIDTH} -B+n -X0 -Y0
          # Create background map
          gmt grdimage @earth_relief_06m -I
          # Create cpt for the earthquakes
          gmt makecpt -Cred,green,blue -T0,70,300,10000
          gmt events @quakes_2018.txt -SE- -C -T${MOVIE_COL0}
        gmt end
        EOF

        gmt movie main.sh -NQuakes -Ml,png -Zs -V -C24cx12cx80 -T2018-01-01T/2018-12-31T/1d -Gblack \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-



3.4. Make draft animation
==========================

In this step, we can make a draft animation. For this example, I recommend making a low quality (with 30 DPC) video to see if the quakes appear correctly.

3.4.1. First attempt
^^^^^^^^^^^^^^^^^^^^^


    .. code-block:: bash

        cat << 'EOF' > main.sh
        gmt begin
          # Set parameters and position
          gmt basemap -Rg -JN${MOVIE_WIDTH} -B+n -X0 -Y0
          # Create background map
          gmt grdimage @earth_relief_06m -I
          # Create cpt for the earthquakes
          gmt makecpt -Cred,green,blue -T0,70,300,10000
          gmt events @quakes_2018.txt -SE- -C -T${MOVIE_COL0}
        gmt end
        EOF

        gmt movie main.sh -NQuakes -Ml,png -Zs -V -C24cx12cx30 -T2018-01-01T/2018-12-31T/1d -Gblack \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=- -Fmp4


..  youtube:: TH4moYCHRT8
    :align: center
    :height: 400px
    :aspect: 2:1


.. Warning::
  - The above script works well but it can be more efficient if a background script is used as well.


3.4.2. The background script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within :gmt-module:`movie` module, there is an optional background (`-Sb <https://docs.generic-mapping-tools.org/dev/movie.html#sb>`_) script that it is used for two purposes:

#. Create files that will be needed by the main script to make the movie.
#. Make a static background plot that should form the background for all frames.

.. admonition:: Technical Information

  The background script is run only once.


3.4.3. Second attempt (with background script)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this step, instead of creating just the main script as before, I now create both a background script and a main script.
The background script (``pre.sh``) is used to:

#. create a CPT file that will be used to color the quakes.
#. make a **static** worldwide background map.

.. Important:: 

  - The animation created is identical to the previous one.
  - The use of a background script allows the creation of the animation much faster because the CPT and the **static** background map will be created only once (instead of 365 times).
..

    .. code-block:: bash

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
          gmt events @quakes_2018.txt -SE- -Cquakes.cpt -T${MOVIE_COL0}
        gmt end
        EOF

        gmt movie main.sh -Sbpre.sh -NQuakes -Ml,png -Zs -V -C24cx12x80 -T2018-01-01T/2018-12-31T/1d -Gblack \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


.. admonition:: Technical Information

  - For the CPT, I must use `-H <https://docs.generic-mapping-tools.org/latest/makecpt.html#h>`_ and give it a name, and then use that name in ``main.sh``.
  - I add ``-Sbpre.sh`` within the :gmt-module:`movie` module to use the background script.
  - I repeat the ``basemap`` command in the main and background scripts so both have the same positioning (i.e., ``-X`` and ``-Y``) and parameters (i.e. ``-R`` and ``-J``).


3.5. Make full animation
=========================

Now I make the final high-quality animation (i.e. 80 DPC).


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

        gmt movie main.sh -Sbpre.sh -NQuakes -Ml,png -Zs -V -C24cx12cx80 -T2018-01-01T/2018-12-31T/1d -Gblack -Fmp4 \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


..  youtube:: dbOjYqWzGi0
    :align: center
    :height: 400px
    :aspect: 2:1

|

3.6. Make full animation with enhancement
=========================================

In the previous animation, the earthquakes appear but it is hard to see when they do it. 
With :gmt-module:`events` is possible to draw attention to the arrival of a new event.

3.6.1. How to enhance symbols with events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The idea is to change the default behavior of the symbols to enhance their appearance as shown in the following video:

..  youtube:: 77a2XrfWsHM
    :align: center
    :height: 400px
    :aspect: 16:9


|

This can be done by using `-M <https://docs.generic-mapping-tools.org/dev/events.html#m>`_ and `-E <https://docs.generic-mapping-tools.org/dev/events.html#e>`_ arguments.
The -M arguments allows to temporarily change attributes of the symbol like:
 
- -Ms: Provide a factor to modify the size.
- -Mc: Provide a value to brighten (up to 1) or darken (up to -1) the `color intensity <https://docs.generic-mapping-tools.org/dev/reference/colorspace.html#artificial-illumination>`_.
- -Mt: Transparency. Set a value between 100 (invisible) to 0 (opaque).

The duration of the temporary changes are control via the `-E <https://docs.generic-mapping-tools.org/dev/events.html#e>`_ argument.

- -Er: rise phase. It takes place before the start of the event.
- -Ep: plateau phase. It takes place after the start of the event.
- -Ed: decay phase. It develops after the plateau phase. If the plateau phase does not occur, then it takes place after the start of the event.


.. Note::

   - For finite symbols there are also *normal* and *fade* phases.
   - It is also possible to change the data value with ``-Mv``. 


3.6.2. Make full animation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this step I announce each quake by magnifying size and whitening the color for a little bit (during the rise phase). 
Later the symbols return to their original properties during the decay phase.
The plateau phase is not used.


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
          gmt events @quakes_2018.txt -SE- -Cquakes.cpt -T${MOVIE_COL0} -Es+r2+d6 -Ms5+c1 -Mi1+c0 -Mt+c0 --TIME_UNIT=d
        gmt end
        EOF

        gmt movie main.sh -Sbpre.sh -NQuakes -Ml,png -Zs -V -C24cx12cx80 -T2018-01-01T/2018-12-31T/1d -Gblack -Fmp4 \
        -Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=-


..  youtube:: rmPhIVzhIgY
    :align: center
    :height: 400px
    :aspect: 2:1


.. admonition:: Technical Information

  - \--TIME_UNIT=d: This sets that the values of -E are in days (d).
  - -Es+r2+d6: This sets the duration of the rise phase and the decay phase.
  - -Ms5+c1: modify the size. The size will increase 5 times during the rise phase and then reduce to the original size in the coda phase.
  - -Mt+c0: modify the transparency. The transparency will remain to 0 at the coda phase. This allows it to be seen after its occurrence.
  - -Mi1+c0: modify the intensity of the color. It gets lighter during the rise phase and then returns to its original color in the coda phase.


4. See also
~~~~~~~~~~~

- The paper about animations which include explanation and examples (`Wessel et al. 2024 <https://doi.org/10.1029/2024GC011545>`_).

- Check the :gmt-module:`movie` and :gmt-module:`events` modules documentation for full technical information.

- See the `GMT animation gallery <https://docs.generic-mapping-tools.org/6.5/animations.html>`_ for more examples.

5. References
~~~~~~~~~~~~~

- Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F., & Tian, D. (2019). The Generic Mapping Tools Version 6. Geochemistry, Geophysics, Geosystems, 20(11), 5556–5564. https://doi.org/10.1029/2019GC008515
- Wessel, P., Esteban, F., & Delaviel-Anger, G. (2024). The Generic Mapping Tools and animations for the masses. Geochemistry, Geophysics, Geosystems, 25, e2024GC011545. https://doi.org/10.1029/2024GC011545.
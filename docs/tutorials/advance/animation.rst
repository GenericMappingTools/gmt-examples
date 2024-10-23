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

1. **Moving objects** (e.g., Earth spinning). It uses the ``gmt movie`` module.
2. **Appearing objects** (e.g., earthquakes). It uses ``gmt movie`` and ``gmt events``.

1.5. Prerequisites
==================

- GMT version 6.1 or later.

2. Tutorial 1. Earth spinning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this tutorial, I will explain the simplest type of animation, 
which only requires ``gmt movie`` module. 
As an example, I will create an animation of the Earth spinning similar to the one below:


Corregir link

..  youtube:: NjSDpQ5S3FM
   :width: 100%


2.1. Goals of the Tutorial
==========================

- Provide a general introduction to creating animations with GMT.
- Explain the most important aspects of using the ``gmt movie`` module.
- Serve as a guide to help beginners understand and troubleshoot potential issues.

2.2. Step-by-step Instructions
==============================

To create an animation, follow these steps:


#. Make first image
#. Make master frame with gmt movie
#. Make draft animation
#. Make full animation


#. `221-make-first-image`_.

#. `222-make-master-frame`_.


2.2.1. Make first image
^^^^^^^^^^^^^^^^^^^^^^^

The first step is to create an image using a standard GMT script that will serve as the base for the animation.

**Step Goal**: Create the first image of the animation.

For this example, we will create a map of the Earth with:

     .. gmtplot::
        :height: 40%

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

The ``gmt movie`` module simplifies most of the steps needed to create an animation 
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
        :height: 40%

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

  The main script is saved into the file ``main.sh`` (using a Here Document), 
  which simplifies the process of handling the main script.

  The previous script is surrounded by these two lines:

  The script is saved into the file ``main.sh`` using a Here Document, 
  which simplifies the process of handling the main script.


  .. code-block:: bash 
    cat <<- 'EOF' > main.sh
    ...
    EOF
  
  * This is use to create a new file (name *main.sh*) with the lines up to the End of File (EOF). This is [Here Document](https://en.wikipedia.org/wiki/Here_document).
  This is helpfull because allow us to have (and edit) the main script and the arguments of GMT MOVIE just using a single file.


2.2.2.3. Fix the Canvas
+++++++++++++++++++++++

We will fix the canvas size to match the map dimensions:

**What is the Canvas?**

Since we are plotting each frame, and GMT users typically make a plot of some standard size (e.g., often a paper size, say A4 or US Letter), we need to understand how to determine what our “paper size” is so we can do our composition correctly. We call this paper the canvas (Figure 1) and it is a setting we control. The canvas setting in the movie module (-C) determines basically two things: The size of your “plot paper” and what resolution (in dots per unit; dpu) at which this canvas is converted to a raster image. You should compose your plots using the given canvas size, and movie will make proper conversions of the canvas to image pixel dimensions.


2.3. Make draft animation
^^^^^^^^^^^^^^^^^^^^^^^^^

2.4. Make full animation
^^^^^^^^^^^^^^^^^^^^^^^^

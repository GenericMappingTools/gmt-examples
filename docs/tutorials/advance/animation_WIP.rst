Making animations backup
------------------------

1. Basic Attributes
~~~~~~~~~~~~~~~~~~~~

1.2. Width
==========

1.2.3. Custom
++++++++++++++


1.1. Titulo sin referencia
^^^^^^^^^^^^^^^^^^^^^^^^^^



**How te set the canvas**:

The easiest way to specify your canvas is to use the presets standard formats. By simply selecting a format, the pixel dimensions and resolution are set. For instance, if you want to make an HD movie, you select -CHD. This will compute the required dpu so that the rasterized frame is 1920 by 1,080—the standard HD movie pixel size. If you want a 4k movie, then -CUHD is your choice. However, if you need a custom canvas (say a portrait movie or a square movie), you will need to tell -C both the dimensions and the resolution. For example, selecting a canvas that is 20 cm square and to be rasterized to 600 × 600 pixels (which means a dpu of 30) would be -C20cx20cx30 (or alternatively -C600x600x30c). The movie command conveniently stores the canvas dimension and resolution settings as parameters (Table 2) that are available to be used in your shell script instead of hardwiring values that you may forget to change if you try another -C setting.

<p align="center">
<img src="Tutorial_1/Canvas.png" width="500" height="auto">
</p>

<p align="center">
<img src="Tutorial_1/Canvas_16x9.png" width="500" height="auto">

| Preset format for 16:9 (alias)   | Pixel dimensions | DPC     | DPI     |
|----------------------------------|------------------|---------|---------|
| 4320p (8k and uhd-2)             | 7680 x 4320      | 320     | 800     |
| 2160p (4k and uhd)               | 3840 x 2160      | 160     | 400     |
| 1080p (fhd and hd)               | 1920 x 1080      | 80      | 200     |
| 720p                             | 1280 x 720       | 53.3333 | 133.333 |
| 540p                             | 960 x 540        | 40      | 100     |
| 480p                             | 854 x 480        | 35.5833 | 88.958  |
| 360p                             | 640 x 360        | 26.6667 | 66.667  |
| 240p                             | 426 x 240        | 17.75   | 44.375  |
</p>

* By default, all frames has an offset of 2.54 cm (or 1 inch) in X and Y.
* I use ``-X0`` and ``-Y0`` to remove it.
* The canvas size is important by two reasons


  * to set the final dimension in pixels of frames/movie (i.e. the quality).
  * set the width (in cm or inches) of the frames.


2.2.2.5. Second attemp. Fix the canvas
++++++++++++++++++++++++++++++++++++++

     .. gmtplot::

        cat << 'EOF' > main.sh
        gmt begin
          gmt grdimage @earth_relief_06m -I -JG0/0/13c -X0 -Y0
        gmt end
        EOF
        gmt movie main.sh -NEarth -C13cx13cx80 -T10 -M0,png -Gblack -V


<p align="center">
  <img src="Tutorial_1/Earth_1b.png" width="auto" height="300">
</p>

2.3. Make draft
^^^^^^^^^^^^^^^

+

#### Movie: eliminating the explicit loop over time

In an animation, the illusion of movement is created by a rapid succession of frames (at least ca. 12 fps) that minimally differ from each other. The key idea in movie is for the user to write a single script (called mainscript) that makes the main idea of the animation and it is used for all frames. To introduce variations in them (otherwise, the movie would be incredibly boring), we use specific frame variables (see Table 2) that will automatically be updated as different frames are built. 

* The movie module creates animations by executing a main frame script for each frame time, making one frame image per frame time.
* The main script uses special variables whose values change with frame number.

* In order to introduce changes in the frames we must use the movie parameters.

**Movie parameters**

Constant parameters: These variables are constants throughout the movie.

| Parameter       |                      Purpose or contents                       |
|:---------------:|:---------------------------------------------------------------|
| MOVIE_NFRAMES   | Total number of frames in the movie (via movie -T)             |
| MOVIE_WIDTH     | Width of the movie canvas                                      |
| MOVIE_HEIGHT    | Height of the movie canvas                                     |
| MOVIE_DPU       | Dots (pixels) per unit used to convert to image (via movie -C) |
| MOVIE_RATE      | Number of frames displayed per second (via movie -D)           |

Variable parameters: These variables are updated for each frame (k, w are column number 0, 1, …).

| Parameter     |             Purpose or contents            |
|:-------------:|--------------------------------------------|
| MOVIE_FRAME   | Number of current frame being processed    |
| MOVIE_TAG     | Formatted frame number (string)            |
| MOVIE_NAME    | Prefix for current frame image             |
| MOVIE_COLk    | Variable k from data column k, current row |
| MOVIE_TEXT    | The full trailing text for current row     |
| MOVIE_WORDw   | Word w from trailing text, current row     |


2.3.2 Second attemp
++++++++++++++++++++


* Now, we use the `MOVIE_FRAME` variable to set the central longitude of the map.
This is a variable parameter, so it will change from 0 to 10.
* It is possible also to use the `MOVIE_WIDTH` parameter to set the widht of the map. 
This is a constant parameter and it will remain fixed (to 13 cm) in all the frames.

```bash
cat << 'EOF' > main.sh
gmt begin
gmt grdimage @earth_relief_06m -I -JG-${MOVIE_FRAME}/0/${MOVIE_WIDTH} -Y0 -X0
gmt end
EOF
gmt movie main.sh -NEarth -C13cx13cx30 -T10 -Mf,png -Gblack -V -Fmp4
```
**Note**: I add a minus sign so the earth spinns in the correct sense.

<p align="center">
<video src="Tutorial_1/Earth_2b.mp4" width="auto" height="300" controls> </video>
</p>

We get our sample animation correct.

2.4. Make full animation
^^^^^^^^^^^^^^^^^^^^^^^^

Once that our simple animation is working you can increment the number of frames (-T) and movie quality (-C).

So, I change the amount of frames to 360 (``-T360``) and increment the resolution to 80 dots per cm (``-C13cx13cx80``).

```bash
cat << 'EOF' > main.sh
gmt begin
 gmt grdimage @earth_relief_06m -I -JG-${MOVIE_FRAME}/0/13c -X0 -Y0
gmt end
EOF

gmt movie main.sh -C13cx13cx80 -T360 -M0,png -NEarth -Gblack -V -Fmp4
```

<p align="center">
  <video src="Tutorial_1/Earth.mp4" width="auto" height="300" controls></video>
</p>

`Video <https://www.youtube.com/watch?v=iWt0yZICKlM&list=PL3GHXjKa-p6VdPql5aReLQZeQDJgWDAY>`_


`GMT Forum <https://forum.generic-mapping-tools.org/>`_


Hint: Be carefull. This step could be quite time (and resources) consuming. By default, `gmt movie` uses all the cores available to speed up the frame creation process. So probably you can't do anything else while GMT is creating all the frames (maybe you can take a break, or have lunch).

3. Tutorial 2. Earthquakes
~~~~~~~~~~~~~~~~~~~~~~~~~~

4. References
~~~~~~~~~~~~~

* Wessel, P., Esteban, F., & Delaviel-Anger, G. (2024). The Generic Mapping Tools and animations for the masses. Geochemistry, Geophysics, Geosystems, 25, e2024GC011545. <https://doi.org/10.1029/2024GC011545>

Technical information:

* gmt movie: <https://docs.generic-mapping-tools.org/6.5/movie.html>

More animations examples:

* GMT animation gallery: https://docs.generic-mapping-tools.org/6.5/animations.html
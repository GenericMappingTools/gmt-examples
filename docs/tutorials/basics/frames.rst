Frames, ticks, titles, and labels
-----------------------

Setting frame, ticks, title, etc., of the plot is handled by the :gmt-module:`-B <basemap#b>` parameter that most plotting modules contain like :gmt-module:`basemap`.

Plot Frame
~~~~~~~~~~

By default, GMT does not add a frame to your plot. For example, we can plot
the coastlines of the world with a Mercator projection:


.. gmtplot::

   gmt begin frames png
      gmt coast -R-180/180/-60/60 -JM25c -W
   gmt end show


To add the default GMT frame style to the plot, add **f** to the :gmt-module:`-B <basemap#b>`.


   .. gmtplot::

      gmt begin frames png
         gmt coast -R-180/180/-60/60 -JM25c -W
         gmt basemap -Bf
      gmt end show


Tick labels
~~~~~~~~~~

In GMT the tick labels are called annotations. Add them by passing **a** through the :gmt-module:`-B <basemap#b>` parameter:

   .. gmtplot::

      gmt begin frames png
         gmt coast -R-180/180/-60/60 -JM25c -W
         gmt basemap -Baf
      gmt end show



Gridlines
~~~~~~~~~~

Add automatic grid lines to the plot by adding **g**:


   .. gmtplot::

      gmt begin frames png
         gmt coast -R-180/180/-60/60 -JM25c -W
         gmt basemap -Bafg
      gmt end show


Title
~~~~~~~~~~

The figure title can be set by passing **+ttitle**:

   .. gmtplot::

      gmt begin frames png
         gmt coast -R-180/180/-60/60 -JM25c -W
         gmt basemap -Bafg
         gmt basemap -B+t"Mercator Map"
      gmt end show

Setting the Region
------------------

In this tutorial we are going to explain how to define the geographical region of maps. 
This is done trough the ``-R`` parameter .
To do so, we will use the simplest way which is when the boundaries are defined by meridians and parallels.

This tutorial covers the following methods: 

* `String of Coordinates`_
* `Global Domain keys`_
* `Codes`_

String of Coordinates
~~~~~~~~~~~~~~~~~~~~~

A string of coordinates can be passed to ``-R``, in the form of xmin/xmax/ymin/ymax. 
This is the standard and most customizable way to specify geographic regions.
For example, to make a map that x-range from 85W to 74W and the y-range to 19N to 24N we should use ``-R-85/-74/19/24``

   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxafg -Byafg -R-85/-74/19/24
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


Global Domain keys
~~~~~~~~~~~~~~~~~~

If you want to make a global map, then you can use one of the following codes 
to quickly specify the global domain:

-Rd
===

* ``-Rd``: Centered at the Prime meridian (0º). It sets the region to -180/180/-90/90.


   .. gmtplot::

      gmt begin region png
         gmt basemap -JN12c -Baf -Rd
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


-Rg
===

* ``-Rg``: Centered at the antimeridian (180º). It sets the region to 0/360/-90/90.

   .. gmtplot::

      gmt begin region png
         gmt basemap -JN12c -Baf -Rg
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


Codes
~~~~~

ISO Codes
=========

If you want to make a map of a country, then you select its region with the two-character ISO-Code.
This indirectly supplies the region by consulting the DCW (`Digital Chart of the World <https://github.com/GenericMappingTools/dcw-gmt?tab=readme-ov-file#dcw-gmt-the-digital-chart-of-the-world-for-gmt>`_) database 
and derives the bounding region given by the code.
For example, to make a map of Cuba we should use ``-RCU``.
Note that in this case, the map will have the exact region of the country.


   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxaf -Byaf -RCU
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


DCW Collection
==============

Alternative, to make a map of another named region (continents, oceans, seas, islands, etc.) NOT include in the ISO codes you can use the 
the three-to-five-character codes of `DCW-Collection  <https://github.com/GenericMappingTools/dcw-gmt/tree/master?tab=readme-ov-file#dcw-collections>`_. For example, to make a map of the Mediterranean Sea we should use ``-RIHO28``:


   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxaf -Byaf -RIHO28
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


Many codes
==========

We could use more than one code to get the region that includes all of them.
For example, if we wish to see all Italy and the Mediterranean Sea, then we should use ``-RIHO28,IT``

   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxaf -Byaf -RIHO28,IT
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


Modifiers
==========
There are 3 modifiers to sligthy change the region encompassed by the codes that can be used. 
In the following examples will be used them to modify the exact region of the Mediterranean Sea (-6.0319/36.2093/30.2662/45.7946).


Modifier +R
+++++++++++

If you want to extend 1 degree the region in all directions, then add ``+R1`` to the code.
This will extend the region to ``-7.0319/37.2093/29.2662/46.7946``.


   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxaf -Byaf -RIHO28+R1
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


Modifier +r
+++++++++++

You can use the ``+r`` modifier if you instead want the region will be rounded to nearest integer degree.
In the following example the region will be extend to ``-7/37/30/46``.

   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxaf -Byaf -RIHO28+r1
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


Modifier +e
+++++++++++

Finally, the ``+e`` modifier is like ``+r`` and expands the final region boundaries to be multiples of increment. 
However, it ensures that the bounding box extends by at least 0.25 times the increment.
In the following example the region will be extend to ``-7/37/30/47``.


   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxaf -Byaf -RIHO28+e1
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


Custom expansion
++++++++++++++++

In the previous examples, the expansion was uniformly in all directions. 
If you want to expand the region differently in each direction, then you could passed four values
(to expands to the west, east, south and north repectively),
For example use the modifier ``+R1/2/3/4`` to expand the Mediterranean Sea map.

   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxaf -Byaf -RIHO28+R1/2/3/4
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show


Shrink region
+++++++++++++

All the above modifiers can be also use to shrink the area. Just use a negative number.
For example use the modifier ``+R-2`` to shrink the Mediterranean Sea map by two degrees.

   .. gmtplot::

      gmt begin region png
         gmt basemap -JM12c -Bxaf -Byaf -RIHO28+R-3
         gmt coast -Glightgray -Swhite -W1/0.5p -N1/0.5p -Clightgray
      gmt end show



How to make a slope map
-----------------------

This tutorial show how to make a slope map of the moon from a geographic grid.

We utilize ``grdgradient`` to calculate the gradient magnitude (i.e., dz/dr).
Since we are working with geographic coordinates (longitude and latitude), 
it is crucial to set the correct ellipsoid parameter (in this case, for the moon). 
Finally, we convert this gradient to degrees with ``grdmath``.

.. gmtplot::

   # Make a slope map of the moon.
   # Calculate gradient magnitude
   gmt grdgradient @moon_relief_15m -D -Sgradient.nc -fg --PROJ_ELLIPSOID=moon
   # Convert gradient to degrees
   gmt grdmath gradient.nc ATAND = moon_slope.nc
   # Make map with colorbar
   gmt begin moon png
    gmt makecpt -Clajolla -T0/12 -I
       gmt grdimage moon_slope.nc -JW15c -B0
       gmt colorbar -DJRM+o0.5c/0c+w90%/0.5c+ef -Ba+l"Slope (@.)"
   gmt end
   # Delete temporal files
   rm gradient.nc
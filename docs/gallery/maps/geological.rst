How to make a geolgical time map
------------------------------------

This example shows how to combine a geological time scale CPT with the age grids


.. gmtplot::

   # How to plot political borders from GADM data set
   #
   # Set geographic region
   REGION=d
   RESOLUTION=05d
   # Set file name without extension
   SHADOW=relief_intensity.nc
   # Calculate gradient magnitude
   gmt grdgradient -R$REGION @earth_relief_05m_p -G$SHADOW -A270 -Ne0.5
   # ------------------------------------
   gmt begin Age png
       gmt grdimage    -R$REGION -JW15c @earth_age_05m_p -I$SHADOW -CCPT
	   gmt colorbar -DJRM+o0.3c/0+w-7/0.618c -C -I -G0/200 -L0 
     # gmt colorbar -DJRM+o0.3c/0+w-7/0.618c -C -I -G0/200 -B+l"Age (Ma)" 
	  # gmt basemap -R -J -O -K >> %OUT% -B0
	   gmt coast -W1/faint
  gmt end
  # Delete temporal files
  rm $SHADOW
    
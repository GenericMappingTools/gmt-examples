How to make a geolgical time map
------------------------------------

This example shows how to combine a geological time scale CPT with the age grids to create a geolgical map.


.. gmtplot::

   # How to plot political borders from GADM data set
   #
   # Set geographic region
   REGION=d
   RESOLUTION=05d
   # Set file name without extension
   SHADOW=relief_intensity.nc
   CPT=epochs.cpt
   # Calculate gradient magnitude
   gmt grdgradient -R$REGION @earth_relief_05m_p -G$SHADOW -A270 -Ne0.5
   # Get CPT
   gmt which -G "http://www.seaviewsensing.com/pub/cpt-city/heine/GTS2012_epochs.cpt" > $CPT   
  #gmt which -G "http://www.seaviewsensing.com/pub/cpt-city/heine/GTS2012_periods.cpt"
   # ------------------------------------
   gmt begin Age png
       gmt grdimage    -R$REGION -JW15c @earth_age_05m_p -I$SHADOW -C$CPT
	   gmt colorbar -DJRM+o0.3c/0+w-7/0.618c -C$CPT -I -G0/200 -L0 
       # gmt colorbar -DJRM+o0.3c/0+w-7/0.618c -C -I -G0/200 -B+l"Age (Ma)" 
	   # gmt basemap -B0
	   gmt coast -W1/faint
  gmt end
  # Delete temporal files
  rm $SHADOW
    
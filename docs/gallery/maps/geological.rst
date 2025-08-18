Visualizing oceanic crustal ages with geological time scale colors
-------------------------------------------------------------------

This example demonstrates how to plot the age of the oceanic crust using the EarthByte age grid combined with the GTS2012 geological time scale color palette. To enhance the visualization, we also compute shading from the Earth relief model and overlay coastlines.


.. gmtplot::

   # Select geological time scale to use
   CPT=GTS2012_epochs.cpt
   # Set geographic region
   REGION=d
   RESOLUTION=05d
   # Set file name without extension
   SHADOW=relief_intensity.nc
   # Calculate gradient magnitude
   gmt grdgradient -R$REGION @earth_relief_05m_p -G$SHADOW -A270 -Ne0.5
   # Get CPT
   gmt which -G "http://www.seaviewsensing.com/pub/cpt-city/heine/${CPT}
  #gmt which -G "http://www.seaviewsensing.com/pub/cpt-city/heine/GTS2012_periods.cpt"
   # ------------------------------------
   gmt begin Age png
       gmt grdimage    -R$REGION -JW15c @earth_age_05m_p -I$SHADOW -C$CPT
	   gmt colorbar -DJRM+o0.3c/0+w-7/0.618c -C$CPT -I -G0/200 -L0 
       # Draw colorbar 
       #gmt colorbar -DJRM+o0.3c/0+w-7/0.618c -C -I -G0/200 -B+l"Age (Ma)" 
       # Improve map with border and shoreline
	   gmt coast -W1/faint -B0
  gmt end
  # Delete temporal files
  rm $SHADOW
    
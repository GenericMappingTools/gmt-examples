Visualizing oceanic crustal ages with the geological time scale
---------------------------------------------------------------

This example demonstrates how to plot the age of the oceanic crust using the EarthByte age grid combined with the GTS2012 geological time scale color palette. To enhance the visualization, we also compute shading from the Earth relief model and overlay coastlines.


.. gmtplot::

   # Select geological time scale to use
   CPT=@GTS2012_epochs.cpt
   # Calculate gradient magnitude from relief grid
   gmt grdgradient @earth_relief_05m_p -Gintens.grd -A270 -Ne0.5
   gmt begin geological png
       gmt grdimage -JW15c @earth_age_05m_p -Iintens.grd -C$CPT
       # Draw colorbar with labels
       gmt colorbar -DJRM+o0.3c/0+w-7/0.618c -C -I -G0/200 -L0 
       # Add border and shorelines
       gmt coast -W1/faint -B0
  gmt end
  # Delete temporal file
  rm intens.grd
    
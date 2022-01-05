Plotting a surface
------------------

:gmt-module:`grdview` can plot 3-D surfaces using the :gmt-module:`-Q <grdview#q>`
parameter with the ``s`` directive. Here, we use :gmt-module:`grdmath` to create
a netCDF file containing a grid for plotting.

Note that the **-p** parameter here controls the azimuth and elevation angle of
the view.

We use the :gmt-module:`-B <grdview#b>` parameter twice - the first specifies
the :math:`x`- and :math:`y`-axes frame attributes and the second specifies the
:math:`z`-axis frame attributes using the ``z`` directive.

The :gmt-module:`-I <grdview#i>` parameter specifies the illumination; here we
use an azimuth of 45° using the ``+a`` modifier.

.. gmtplot::
   :language: bash

   gmt grdmath -R-15/15/-15/15 -I0.3 X Y HYPOT DUP 2 MUL PI MUL 8 DIV COS EXCH NEG 10 DIV EXP MUL 0.001 SUB = example_grid.nc
   gmt begin grdview_surface png
      gmt grdview example_grid.nc -Ba5f1 -Bza5f1 -JX10C -JZ2c -Qs -Croma -p135/30 -I+a45
   gmt end show

How to use political borders from GADM
---------------------------------------

GADM (https://gadm.org/) is a project that provides spatial data for all countries and their sub-divisions. 
They allow you to freely use their data (see `license <https://gadm.org/license.html>`_) to make your own maps. 
You can use this script to download the data from their server.
You only need to select a data set (using a three-letter code) and a level. 
Not all levels are available. Check first in their website if the data set exists. 
Here is a table with the number of file available for each level. 

 ======= ============ 
  Level   # of files  
 ======= ============ 
  0       254         
  1       230         
  2       171         
  3       69          
  4       21          
  5       2           
 ======= ============ 

The script will download the selected data and level in KMZ format. 
Then, it will unzip that file (to KML) and convert it to a GMT format.
At the end, you will have a GMT file in the same directory.
To demostrate, we will create a level 1 map of Mexico (code MEX).

.. gmtplot::

   # How to plot political borders from GADM data set
   #
   # GDAM data
   # ------------------------------------
   # Set country with three-leter code.
   COUNTRY=MEX
   # Set level from 0 to 5. 0 = Country outline.
   LEVEL=1
   # GADM data set version
   VERSION=4.1
   # File formats (https://gadm.org/formats.html)
   FORMAT=kmz
   SITE="https://geodata.ucdavis.edu/gadm/"
   # Remove dot from version
   VERSION_WITHOUT_DOT=$(echo ${VERSION} | tr -d '.')
   # Set file name without extension
   NAME="gadm${VERSION_WITHOUT_DOT}_${COUNTRY}_${LEVEL}"
   # URL
   URL="${SITE}gadm${VERSION}/${FORMAT}/${NAME}.${FORMAT}"
   # ------------------------------------
   # Download data from GADM
   echo "Downloading geographic data provided by the https://gadm.org project. It may take a while."
   gmt which $URL -Gc
   # Unzip KMZ to KML. Set to NOT (-n) overwrite existing file.
   unzip -n ${NAME}.${FORMAT}
   # Convert KML file to GMT format with OGR/GDAL
   ogr2ogr -f "GMT" ${NAME}.gmt ${NAME}.kml
   # Test Plot data
   gmt begin ${COUNTRY} png
       gmt plot ${NAME}.gmt -Wred -JM15c -Bf -Re
   gmt end
   # Delete KMZ and KML files
   rm ${NAME}.km?
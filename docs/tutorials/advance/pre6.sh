lon=0
while [ ${lon} -lt 360 ]; do
	gmt begin frame_${lon} tif
	    gmt grdimage @earth_relief_06m -I -JG${lon}/0/13c
	gmt end
	lon=`expr ${lon} + 1`
done
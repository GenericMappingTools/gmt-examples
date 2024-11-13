cat << 'EOF' > main.sh
gmt begin
# Set parameters and position
gmt basemap -Rg -JN${MOVIE_WIDTH} -B+n -X0 -Y0
# Create background map
gmt grdimage @earth_relief_06m -I
# Create cpt for the earthquakes
gmt makecpt -Cred,green,blue -T0,70,300,10000
gmt events @quakes_2018.txt -SE- -C -T${MOVIE_COL0}
gmt end
EOF

gmt movie main.sh -NEarth -Ml,png -Zs -V -C24cx12cx30 -T2018-01-01T/2018-12-31T/1d -Gblack \
-Lc0 --FONT_TAG=18p,Helvetica,white --FORMAT_CLOCK_MAP=- -Fmp4

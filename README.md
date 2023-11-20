# Folder Structure

processed-tables 
-
- merge21.csv 
    - The csv generated from gis processing of the data, the output information contains intersected area of each buffer on the census 2021 DA boundary

- merge96.csv
    - The csv generated from gis processing of the data, the output information contains intersected area of each transit point buffer on the census 1996 enumeration boundary 

- transit-station-reorder
    - this file reorders the transit points, the output file arranges the points from east to west for some transit lines, but we want to present the transit points from west to east, just like how we see them on transit maps. 

input-files
- 
- Census1996.csv - 
    -  Census data for 1996 downloaded from CHASS platfrom hosted by the University of Toronto. 

- Census2021.csv - 
    - Census data for 2021 downloaded from CHASS platfrom hosted by the University of Toronto. 

- transit-line-points.csv - 
    - a csv with all the coordinates of the points generated (one point every 400m)

- transit-station-distance.csv - 
    - a csv with the distance from the origin of the transit line (i.e Kipling is 0m from the start of the Bloor-Danforth line, Islington is 1358m away from the start of Bloor-Danforth line)

python codes
- 
 - gis-processing.py
    - currently an arcpy code, will be updated to non-arcpy at a later date
 - process.ipynb
    - python file that uses pandas to process merge21 and merge95 to produce the results. The output from this code is data.json and station-distance.json.

data
- 
- data.json
    - the data file that contains census information for each transit point. 
- station-distance.json
    - contains the json version of transit-station-distance.csv
- transit-lines.geo.json
    - input file for map.svelte, contains transit-line layer 
- transit-station.geo.json
    - input file for map.svelte, contains transit station layer

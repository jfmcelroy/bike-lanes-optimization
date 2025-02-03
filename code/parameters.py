#threshold = 200 # radius for arcs (origin,intermediate) or (intermediate,dest)
# replace threshold variable with stratified list of radii for arcs (origin,intermediate) or (intermediate,dest)

radii = [50,100,150,200,250,300,400]  
# 301 bc there's one single block that is 371.something meters away from bike nodes (once motorways excluded)

# CRS projection for distance calculations?
# currently using Albers contiguous USA
#'ESRI:102003'

# budget 

# upgrade costs (in $million/mile)
cost_per_mile = 2 * 10**6 # $2mil/mi
cost_per_mile_modi = 2 * 10**6 # $2mil/mi; if not in H2 
cost_per_mile_bidi = 1 * 10**6 # $1mil/mi; if in H2 
# convert to $/m
cost_per_meter = cost_per_mile/1609.34
cost_per_meter_modi = cost_per_mile_modi/1609.34
cost_per_meter_bidi = cost_per_mile_bidi/1609.34

# exceedance factor f

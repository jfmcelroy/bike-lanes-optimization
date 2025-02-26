# radii to connect nodes from different data sets 
radii = [50,100,150,200,250,300,400]  

# coordinate reference systems
#cycle_network_crs = 'EPSG:4326'
distance_crs = 'ESRI:102003' # Albers contiguous USA, for distance calculations

# budget as a proportion of total cost
total_cost_proportion = 0.15

# upgrade costs (in $million/mile)
cost_per_mile = 2 * 10**6 # $2mil/mi
cost_per_meter = cost_per_mile/1609.34

# factor by which a low stress path would need to exceed a high stress route in order for someone to choose the shorter high stress route. 
# equiv: someone would be willing f times further in order to stay on a low stress path
# see https://transweb.sjsu.edu/sites/default/files/1005-low-stress-bicycling-network-connectivity.pdf
# page 3
f = 1.25 
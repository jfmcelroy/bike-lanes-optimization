# Lexington-Fayette-Urban County Government Urban Service Area
# https://hub.arcgis.com/datasets/4c8db8e014cb49349fd430d96d8994b9_0/about
city_boundary_gdf = (
    gpd.read_file('data/lfucg_usb/Urban_Service_Area.shp')
    .to_crs('EPSG:4326') # project to classic CRS
)
city_boundary=city_boundary_gdf.geometry.iloc[0]

# US census data
# census block geometry
census_blocks_gdf = (
    gpd
    .read_file('data/tl_2020_21067_tabblock20/tl_2020_21067_tabblock20.shp')
    .assign(in_USB=lambda df: df['geometry'].within(city_boundary)) # define a truth column
    .query("in_USB == True") # select only blocks inside the USB
    .query("GEOID20 != '210670040061008'") # exclude a specific block 
    # the above block is rural in appearance, and quite far from any bike network nodes (770m)
)
# population data
population_df = (
    pd
    .read_csv('data/DECENNIALPL2020.H1_2024-04-02T135509/DECENNIALPL2020.H1-Data.csv')
    .query('GEO_ID != "Geography"') # data has a "header" row
    .drop_duplicates() # original data has 101 duplicate rows 
)
# https://api.census.gov/data/2020/dec/pl/variables.html for more info 

# list of arcs to remove from the bike network
arc_exclude_list = [
    83568, # disconnects census block 210670026005001
    126616, # golf course; disconnects census block 210670019001020
    126608, # golf course; disconnects census block 210670019001003
    126612, # golf course; disconnects census block 210670019001002
    60836, # parking lot; disconnects census block 210670019002002
    60835, # parking lot; disconnects census block 210670019002002
    62039, # parking lot; disconnects census block 210670019002002
    79572, # parking lot; disconnects census block 210670010002002
    85764, # parking lot; disconnects census block 210670010002002
    116486, # sidewalk; disconnects census block 210670039084042
    98492, # sidewalk; disconnects census block 210670039084042
    126711, # golf course; disconnects census block 210670034052004
    126398, # golf course; disconnects census block 210670034052003
    81467, # parking lot; disconnects census block 210670041053003 
    81468, # parking lot; disconnects census block 210670041053003 
    81469, # parking lot; disconnects census block 210670041053003 
    81471, # parking lot; disconnects census block 210670041053003 
    81472, # parking lot; disconnects census block 210670041053003 
    81477, # parking lot; disconnects census block 210670041053003 
    119911, # parking lot; disconnects census block 210670041053003 
    59819, # sidewalk; disconnects census block 210670001011027
    57257, # sidewalk; disconnects census block 210670001011027
    59818, # sidewalk; disconnects census block 210670001011008
    65637, # parking lot; disconnects census block 210670003003006
    50229, # sidewalk; disconnects census block 210670004002004
    50111, # sidewalk; disconnects census block 210670004002004
    59541, # sidewalk; disconnects census block 210670018002015
    54569, # sidewalk; disconnects census block 210670018002015
    54180, # sidewalk; disconnects census block 210670008022002
    73268, # parking lot; disconnects census block 210670007001013
    73296, # parking lot; disconnects census block 210670007001013
    73294, # parking lot; disconnects census block 210670007001013
    73292, # parking lot; disconnects census block 210670007001013
    71562, # parking lot; disconnects census block 210670007002002
    74034, # parking lot; disconnects census block 210670007002002
    126440, # golf course; disconnects census block 210670017002000
    126441, # golf course; disconnects census block 210670017002000
    126442, # golf course; disconnects census block 210670017002000
    126443, # golf course; disconnects census block 210670017002000
    126444, # golf course; disconnects census block 210670017002000
    126445, # golf course; disconnects census block 210670017002000
    126446, # golf course; disconnects census block 210670017002000
    126447, # golf course; disconnects census block 210670017002000
    126448, # golf course; disconnects census block 210670017002000
    126449, # golf course; disconnects census block 210670017002000
    126450, # golf course; disconnects census block 210670017002000
    81470, # parking lot; disconnects census block 210670041053003
    83569, # parking lot; disconnects census block 210670026005001
    83571, # parking lot; disconnects census block 210670026005001
    83569, # parking lot; disconnects census block 210670026005001
    62068, # parking lot; disconnects census block 210670019002002
    62071, # parking lot; disconnects census block 210670019002002
    60837, # parking lot; disconnects census block 210670019002002
    50232, # sidewalk; disconnects census block 210670004002004
    58492, # sidewalk; disconnects census block 210670004002004
    126397, # golf course; disconnects census block 210670034052003
    58109, # sidewalk; disconnects census block 210670001021003; maybe
    59254, # sidewalk;disconnects census block 210670001021003; maybe
    126396, # golf course; disconnects census block 210670034052003
    126397, # golf course; disconnects census block 210670034052003
    126710, # golf course; disconnects census block 210670034052003
    71233, # golf course; disconnects census block 210670034052003
    72867, # golf course; disconnects census block 210670034052003
    72868, # golf course; disconnects census block 210670034052003
    72869, # golf course; disconnects census block 210670034052003
    72870, # golf course; disconnects census block 210670034052003
    79919, # parking lot; disconnects census block 210670040013000; maybe
    79918, # parking lot; disconnects census block 210670040013000; maybe
    79921, # parking lot; disconnects census block 210670040013000; maybe
    79917, # parking lot; disconnects census block 210670040013000; maybe
    114815, # parking lot; disconnects census block 210670032021009; maybe
    109752, # parking lot; disconnects census block 210670032021009; maybe
    109753, # parking lot; disconnects census block 210670032021009; maybe
    106337, # parking lot; disconnects census block 210670038023034; maybe
    106339, # parking lot; disconnects census block 210670038023034; maybe
    106338, # parking lot; disconnects census block 210670038023034; maybe
    101567, # parking lot; disconnects census block 210670038023034; maybe
    106340, # parking lot; disconnects census block 210670038023034; maybe
]

# PeopleForBikes cycle network data
pfb_gdf = (
    gpd.read_file('data/people_for_bikes/neighborhood_ways/neighborhood_ways.shp')
    .query('ROAD_ID not in @arc_exclude_list') # remove disconnected edges from the network
    .query("FUNCTIONAL != 'motorway'") # remove the highways
    .query("FUNCTIONAL != 'motorway_link'") # exit ramps etc.
)

# list of amenities to exclude based on local knowledge
# consider editing the source file directly 
dest_exclude_list = [
    'node/12001067429', # 'The Venue Shopping Center Courtyard' is not a real park
    'node/8520821500', # Speigle Heights Park has a node and a way
    'node/12001059631', # Zandale Park has a node and a way
    'node/3197373270' # Red Mile Horse training area isn't a 'park' in the sense we care about
]

# amenity data
amenities_gdf = (
    gpd
    .read_file("data/lex_parks_export.geojson") # from Overpass Turbo
    .cx[-84.6 : -84.3,  37.9 : 38.2] # filter non-KY Lexingtons using a bounding box
    .query('id not in @dest_exclude_list') # remove individual entries
    # consider adding (or replacing) this filter with the Urban Service Boundary
)

# merge geo and pop data
origin_nodes_df = (
    # call population data
    population_df
    .assign(
        geoid20=lambda x: x['GEO_ID'].str.slice(9, 24), # reformat the geoid to match geoblocks_df
        H1_001N=lambda x: x['H1_001N'].astype(int) # convert to integer
    ) 
    
    # merge with census blocks geographic data 
    .merge(census_blocks_gdf, left_on='geoid20', right_on='GEOID20', how='left') 

    # create new columns
    .assign(
        name = lambda x: x['GEOID20'].str[-8:], # last eight digits of GEOID20
        node_type = 'origin'
    )

    # rename columns 
    .rename(columns={
        'GEOID20' : 'id_string',
        'H1_001N' : 'netflow', 
        'INTPTLAT20' : 'lat', 
        'INTPTLON20' : 'lon'
    })

    # select nodes with nonzero population
    .query("netflow > 0")

    # select points inside USB
    # this may be redundant given the query in census_blocks_gdf import 
    .assign(
        # define a Point so we can apply .within()
        geometry=lambda df: df.apply(
            lambda x: Point(x['lon'], x['lat']) if (pd.notna(x['lon']) and pd.notna(x['lat'])) else None,
            axis=1
        ),
        # define a truth column
        in_USB=lambda df: df['geometry'].apply(lambda point: city_boundary.contains(point))
    )
    .query("in_USB == True")

    # reset index — this removes skips in the index
    .reset_index()
    
    # select columns
    [['id_string','name','node_type','netflow','lat','lon']]
)

# calculate the total population (for destination, dummy netflows)
# only include population from inside USB
total_pop = origin_nodes_df['netflow'].sum()

# old code
#old_total_pop = population_df['H1_001N'].astype(int).sum() # 148367

# pull PFB cycling network intersections

# heads 
heads_identifiers_gdf = (
    pfb_gdf
    
    # select columns
    [['INTERSECTI','geometry']]
    
    # change data types, create new columns
    .assign(
        identifier = lambda x: x['INTERSECTI'].astype(int),
        geometry = lambda x: (x['geometry'].to_crs("EPSG:4326")), # convert to classic CRS
        coord = lambda x: (x['geometry'].apply(
            lambda line: (line.coords[0][1], line.coords[0][0]) if line else None) # grab first coord, switch order
        )
    )

    # select points inside USB
    .assign(
        # define a truth column
        in_USB=lambda df: df['geometry'].apply(lambda point: city_boundary.contains(point))
    )
    .query("in_USB == True")

    # re-select columns
    [['identifier','coord']]
)

# tails
tails_identifiers_gdf = (
    pfb_gdf
    
    # select columns
    [['INTERSE_01','geometry']]
    
    # change data types, create new columns
    .assign(
        identifier = lambda x: x['INTERSE_01'].astype(int),
        geometry = lambda x: (x['geometry'].to_crs("EPSG:4326")), # convert to classic CRS
        coord = lambda x: (x['geometry'].apply(
            lambda line: (line.coords[-1][1], line.coords[-1][0]) if line else None) # grab last coord, switch order
        )
    )

    # select points inside USB
    .assign(
        # define a truth column
        in_USB=lambda df: df['geometry'].apply(lambda point: city_boundary.contains(point))
    )
    .query("in_USB == True")

    # re-select columns
    [['identifier','coord']]
)
# combine into single (g)df
intermediate_nodes_df = (
    # concat
    pd.concat([heads_identifiers_gdf, tails_identifiers_gdf], axis=0, ignore_index=True)

    # remove duplicates — this can cause skips in the index
    .drop_duplicates()

    # reset index — this removes skips in the index
    .reset_index()

    # create new columns
    .assign(
        name = '', # blank for now, we just need this column to match the amenity gdf
        node_type = 'intermediate',
        netflow = 0, 
        lat = lambda x: x['coord'].apply(lambda x: x[0] if x else None),
        lon = lambda x: x['coord'].apply(lambda x: x[1] if x else None) 
    )

    # rename columns 
    .rename(columns={'identifier' : 'id_string'})

    # select columns
    [['id_string','name','node_type','netflow','lat','lon']]
)

# pull OSM aminities
# for now we're querying externally via Overpass Turbo
# using parks to start

# open file from overpass turbo
dest_nodes_df = (
    amenities_gdf

    # create new columns
    .assign(
        node_type = 'destination',
        rep_point = lambda x: x['geometry'].representative_point(), # define representative point
        netflow = 0, 
        lat = lambda x: x['rep_point'].apply(lambda point: point.y if point else None), # extract lat
        lon = lambda x: x['rep_point'].apply(lambda point: point.x if point else None) # extract lon
    )

    # rename columns 
    .rename(columns={'id' : 'id_string'})

    # select points inside USB
    .assign(
        # define a truth column
        in_USB=lambda df: df['geometry'].apply(lambda point: city_boundary.contains(point))
    )
    .query("in_USB == True")

    # reset index — this removes skips in the index
    .reset_index()

    # select columns
    [['id_string','name','node_type','netflow','lat','lon']]
)

# create dummy node (sink)
new_row = gpd.GeoDataFrame(
    {
        'id_string': 'dummy_node', # name it
        'name': 'dummy_node', 
        'node_type' : 'dummy_node',
        'netflow': -1*total_pop, # this balances the negative flows of the amenities, like a sink
        'lat': [0], # put it somewhere not in the network?
        'lon': [0] # put it somewhere not in the network?
    }
)

# combine into single gdf
nodes_df = pd.concat([origin_nodes_df, intermediate_nodes_df, dest_nodes_df, new_row], ignore_index=True)

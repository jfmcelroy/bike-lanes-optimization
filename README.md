# bike-lanes-optimization

Riding bikes is a crucial piece of a larger transportation sustainability puzzle. Bikes are some of the most energy-efficient machines we have. 
In cities with car-prioritizing infrastructure (e.g. most US cities, including Lexington), choosing bike routes that feel safe can involve considerable detours. 
Fortunately, many cities have begun retrofitting car-centric infrastructure with more bike-friendly features. 
The optimization model we produce gives a potential answer to the question "What are the best roads on which to build bike-friendly infrastructure to minimize the amount of safety-detouring?" 

# Stress

The organization PeopleForBikes has classification criteria that groups bike routes in to high stress and low stress, detailed [here](https://cityratings.peopleforbikes.org/about/methodology).
This theory of high- and low-stress networks is based on [work by Mekuria, Furth and Nixon](https://transweb.sjsu.edu/research/Low-Stress-Bicycling-and-Network-Connectivity).
These criteria include things like speed limit and number of lanes. 
PeopleForBikes have applied these criteria to many cities, [including Lexington, KY, USA](https://bna.peopleforbikes.org/#/places/f12b7872-ac3a-47e8-9c24-f06774b0e2a0/), pictured below. 

![PeopleForBikes stress analysis of Lexington, KY, USA.](/data/images/pfb_lex.png)

# Upgrades

This model assumes that a city has a budget dedicated towards upgrading the bicycle network.  
In this model, this is equivalenet to changing a high-stress segment to low-stress (assuming the design of the project is sufficient to attain low-stress classification). 

# Flow

The model uses a network flow setup, which imagines people `flowing' from origins to destinations.
In the first version of the Lexington model, we use US census blocks as origins and parks as destinations. 
One could just as well use other amenities as destinations, (e.g. grocery stores, libraries, etc.). 

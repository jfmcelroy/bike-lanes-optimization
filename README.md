# bike-lanes-optimization

Riding bikes is a crucial piece of a larger transportation sustainability puzzle. Bikes are some of the most energy-efficient machines we have. 
In cities with car-prioritizing infrastructure (e.g. most US cities, including Lexington, KY), choosing bike routes that feel safe can involve considerable detours. 
Fortunately, many cities have begun retrofitting car-centric infrastructure with more bike-friendly features. 
The optimization model we produce seeks to answer to the question "What are the best roads on which to build bike-friendly infrastructure to minimize the amount of safety-detouring?" 

# Authors

[James Ford McElroy](https://sites.google.com/view/jamesfordmcelroy) is a Ph.D. student at the University of Kentucky in Lexington, studying mathematics and interested in transportation justice. 
[Dr. Daphne Skipper](https://sites.google.com/usna.edu/daphneskipper) is an Associate Professor at the U.S. Naval Academy and an expert in optimization. 

# Stress

The organization [PeopleForBikes](https://www.peopleforbikes.org/) has classification criteria that groups bike routes into high stress and low stress segments, detailed [here](https://cityratings.peopleforbikes.org/about/methodology).
This theory of high- and low-stress bike infrastructure is based on [work by Mekuria, Furth and Nixon](https://transweb.sjsu.edu/research/Low-Stress-Bicycling-and-Network-Connectivity).
Classification criteria include route characteristics like speed limit and number of lanes. 
PeopleForBikes have applied these criteria to many cities, [including Lexington, KY, USA](https://bna.peopleforbikes.org/#/places/f12b7872-ac3a-47e8-9c24-f06774b0e2a0/), pictured below, with low-stress segments shown in blue and high-stress segments shown in red. 

![PeopleForBikes stress analysis of Lexington, KY, USA.](/data/images/pfb_lex.png)

# Upgrades

This model assumes that a city has a budget dedicated to upgrading the bicycle network.  
In the model, there is a cost to upgrade each high-stress segment of the bike network to low-stress. The model seeks the optimal set of network upgrades given a fixed budget.

# Flow

The model uses network flow constraints, which imagines people traveling as 'flow' from origins to destinations.
In the first version of the Lexington model, we use US census blocks as origins and parks as destinations. 
Thus, we seek to upgrade the network to improve the average bike ride from a residence to the closest park as much as possible.
One could replace parks with other amenities as destinations, such as grocery stores, libraries, etc. 

# Optimization

An optimization model requires three basic elements: an objective function, decision variables, and constraints.
The objective function quantifies the goal. 
The decision variables allow every scenario to be to be modeled by objective function. 
The constraints make sure the scenarios over which the decision variables range correspond to viable decisions. 

A detailed explanation of the optimization model can be found in the [model_mathematics.pdf](model_mathematics.pdf) file. 

# Code

This repository contains the code being used to solve the model (main_solver).
However, as of 2025-Feb-3, the code is still in the debugging process. 

import osmnx as ox # open street maps
import geopandas as gpd # geodata wrangling
import pandas as pd # data wrangling
import numpy as np
import pyomo.environ as pyo 
import shapely # even more geodata wrangling
import gurobipy as gp # solver 2
import json # save solution 
from gurobipy import GRB 
from collections import defaultdict 
from scipy.spatial.distance import cdist # makes the distance matrix computation fast
from shapely.geometry import LineString # creates LineString geometry objects
from shapely.geometry import Point # creates Point geometry objects
from pyomo.environ import * # import Var

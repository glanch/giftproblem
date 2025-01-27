import json 

from knapsack import solve_knapsack
from regression.lad import regress_lad
from regression.ls import regress_ls

def print_packed_items(packed_items):
    print("Packed items:")
    print(" ".join(packed_items))

# Read packages and items
with open("data/packages.json", "r") as f:
    packages = json.load(f)

with open("data/items.json", "r") as f:
    items = json.load(f)

# Create item dict
items_dict = {}
for item in items:
    item_name = item["name"]
    assert item_name not in items_dict
    items_dict[item_name] = item

# Check for assumptions and process data 
packages_dict = {}
for index, package in enumerate(packages):
    for item_name in package["items"]:
        assert item_name in items_dict

    package_name = str(index)
    package["name"] = package_name
    package["items"] = set(package["items"])

    packages_dict[package_name] = package
    

TOTAL_BACKPACK_SIZE = 40

# Estimate volumes using Least Squares (LS) or Least Absolute Deviation (LAD)
USE_LS = True
USE_LAD = False

if USE_LS:
    print("")
    print("Estimating item volumes with LS")
    estimated_volumes_ls = regress_ls(items_dict, packages_dict)
    print("Solving knapsack for LS")
    optimal_objective_ls, packed_items_ls = solve_knapsack(TOTAL_BACKPACK_SIZE, items_dict, packages_dict, estimated_volumes_ls)
    print_packed_items(packed_items_ls)

if USE_LAD:
    print("")
    print("Estimating item volumes with LAD")
    estimated_volumes_lad = regress_lad(items_dict, packages_dict)
    print("Solving knapsack for LAD")
    optimal_objective_lad, packed_items_lad = solve_knapsack(TOTAL_BACKPACK_SIZE, items_dict, packages_dict, estimated_volumes_lad)
    print_packed_items(packed_items_lad)
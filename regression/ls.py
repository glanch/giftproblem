from numpy import array, dot
from qpsolvers import solve_ls

def regress_ls(items_dict, packages_dict):
    R = array([[(1. if item in package["items"] else 0.) for item in items_dict.keys()] for package in packages_dict.values()])
    s = array([package["total_volume"] for package in packages_dict.values()])
    G = None
    h = None

    x_sol = solve_ls(R, s, G, h, solver="gurobi")

    estimated_volumes = {}
    for item_index, (item_name, item) in enumerate(items_dict.items()):
        item_value = x_sol[item_index]
        estimated_volumes[item_name] = item_value

    return estimated_volumes
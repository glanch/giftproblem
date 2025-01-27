from gurobipy import Model, GRB, quicksum

def regress_lad(items_dict, packages_dict):
    # Model: 
    model = Model("calculate_volumes")
    model.ModelSense = GRB.MINIMIZE

    # Variable for each package that indictates absolute error
    for package_name, package in packages_dict.items():
        package["positive_error_variable"] = model.addVar(lb=0, ub=float("inf"), obj=1, name=f"positive_error_{package_name}")
        package["negative_error_variable"] = model.addVar(lb=0, ub=float("inf"), obj=1, name=f"negative_error_{package_name}")

    for item_name, item in items_dict.items():
        item["variable"] = model.addVar(lb=0, ub=float("inf"), obj=0, name=f"{item["name"]}")

    model.update()
    
    for package_name, package in packages_dict.items():
        package["slack_constraint"] = model.addConstr(package["positive_error_variable"] - package["negative_error_variable"] + package["total_volume"]== quicksum([items_dict[item_name]["variable"] for item_name in package["items"]]))

    model.optimize()

    if model.status == GRB.OPTIMAL:
        estimated_volumes = {}

        for item_name, item in items_dict.items():
            item_value = item["variable"].X
            estimated_volumes[item_name] = item_value    

        return estimated_volumes
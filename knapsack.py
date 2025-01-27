from gurobipy import Model, GRB, quicksum

def solve_knapsack(knapsack_capacity, packing_items_more_than_once_allowed, items_dict, packages_dict, estimated_volumes):
    knapsack_model = Model("gift_knapsack")
    knapsack_model.ModelSense = GRB.MAXIMIZE

    for item_name, item in items_dict.items():
        item["knapsack_packing_variable"] = knapsack_model.addVar(name=f"pack_item_{item_name}", vtype=GRB.INTEGER if packing_items_more_than_once_allowed else GRB.BINARY, lb=0, obj=item["price"])

    TOTAL_KNAPSACK_VOLUME = 40
    knapsack_model.addConstr(quicksum(estimated_volumes[item_name] * item["knapsack_packing_variable"] for item_name, item in items_dict.items()) <= knapsack_capacity)

    knapsack_model.optimize()
    if knapsack_model.status == GRB.OPTIMAL:
        print("Optimal solution for knapsack found")
        
        actual_volume = 0
        actual_price = 0
        
        packed_items = {}
        for item_name, item in items_dict.items():
            item_value = item["knapsack_packing_variable"].X
            
            if item_value > 0.5:
                packed_items[item_name] = round(item_value)
                actual_volume += packed_items[item_name] * estimated_volumes[item_name]
                actual_price += item["price"]

        print(f"Estimated total volume: {actual_volume}/{knapsack_capacity}")
        print(f"Actual price: {actual_price}")

        optimal_objective  = knapsack_model.ObjVal
        print(f"Optimal objective: {optimal_objective}")
        
        return optimal_objective, packed_items


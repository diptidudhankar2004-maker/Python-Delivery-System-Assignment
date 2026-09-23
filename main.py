import json
import math
import sys


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_nearest_agent(warehouse_location, agents):
    nearest_agent = None
    shortest_distance = float("inf")

    for agent_id, agent_location in agents.items():

        distance = calculate_distance(
            agent_location,
            warehouse_location
        )

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_agent = agent_id

    return nearest_agent


# --------------------------------------------------
# 1. Get input file
# --------------------------------------------------

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = "base_case.json"


# --------------------------------------------------
# 2. Read JSON
# --------------------------------------------------

with open(input_file, "r") as file:
    data = json.load(file)


# --------------------------------------------------
# 3. Read agents
# --------------------------------------------------

agents = {}

if isinstance(data["agents"], list):

    for agent in data["agents"]:
        agents[agent["id"]] = agent["location"]

else:

    agents = data["agents"]


# --------------------------------------------------
# 4. Read warehouses
# --------------------------------------------------

warehouses = {}

if isinstance(data["warehouses"], list):

    for warehouse in data["warehouses"]:
        warehouses[warehouse["id"]] = warehouse["location"]

else:

    warehouses = data["warehouses"]


# --------------------------------------------------
# 5. Find nearest agent for each warehouse
# --------------------------------------------------

warehouse_agents = {}

for warehouse_id, warehouse_location in warehouses.items():

    nearest_agent = find_nearest_agent(
        warehouse_location,
        agents
    )

    warehouse_agents[warehouse_id] = nearest_agent


# --------------------------------------------------
# 6. Create result for every agent
# --------------------------------------------------

agent_results = {}

for agent_id in agents:

    agent_results[agent_id] = {
        "packages_delivered": 0,
        "total_distance": 0.0
    }


# --------------------------------------------------
# 7. Process packages
# --------------------------------------------------

for package in data["packages"]:

    package_id = package["id"]

    # Base case uses "warehouse_id"
    # Test cases use "warehouse"

    if "warehouse_id" in package:
        warehouse_id = package["warehouse_id"]
    else:
        warehouse_id = package["warehouse"]

    destination = package["destination"]

    # Find assigned agent
    agent_id = warehouse_agents[warehouse_id]

    # Get locations
    agent_location = agents[agent_id]
    warehouse_location = warehouses[warehouse_id]

    # Agent -> Warehouse
    agent_to_warehouse = calculate_distance(
        agent_location,
        warehouse_location
    )

    # Warehouse -> Destination
    warehouse_to_destination = calculate_distance(
        warehouse_location,
        destination
    )

    # Total distance
    total_distance = (
        agent_to_warehouse +
        warehouse_to_destination
    )

    # Update agent results
    agent_results[agent_id]["packages_delivered"] += 1

    agent_results[agent_id]["total_distance"] += total_distance


# --------------------------------------------------
# 8. Calculate efficiency
# --------------------------------------------------

for agent_id in agent_results:

    packages = agent_results[agent_id]["packages_delivered"]
    total_distance = agent_results[agent_id]["total_distance"]

    if packages > 0:
        efficiency = total_distance / packages
    else:
        efficiency = 0

    agent_results[agent_id]["efficiency"] = efficiency


# --------------------------------------------------
# 9. Find best agent
# --------------------------------------------------

agents_with_packages = {
    agent_id: result
    for agent_id, result in agent_results.items()
    if result["packages_delivered"] > 0
}

if agents_with_packages:

    best_agent = min(
        agents_with_packages,
        key=lambda agent_id:
        agents_with_packages[agent_id]["efficiency"]
    )

else:

    best_agent = None


# --------------------------------------------------
# 10. Round numbers
# --------------------------------------------------

for agent_id in agent_results:

    agent_results[agent_id]["total_distance"] = round(
        agent_results[agent_id]["total_distance"],
        2
    )

    agent_results[agent_id]["efficiency"] = round(
        agent_results[agent_id]["efficiency"],
        2
    )


# --------------------------------------------------
# 11. Add best agent
# --------------------------------------------------

agent_results["best_agent"] = best_agent


# --------------------------------------------------
# 12. Save report
# --------------------------------------------------

with open("report.json", "w") as file:

    json.dump(
        agent_results,
        file,
        indent=4
    )


print("Report generated successfully!")
print("Input file:", input_file)
print("Best agent:", best_agent)
print("Output: report.json")
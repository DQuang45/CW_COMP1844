import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


# ==========================================
# setting up the graph and positions
# ==========================================
unit = input("Choose distance unit (km/miles): ").strip().lower()
if unit not in ["km","miles"]:
    unit = "km"


my_graph = nx.Graph()

# 1. define edges with distances (km)
green_edges_data = [("25", "Jurong_East", 1.5), ("Jurong_East", "23", 3.5), ("23", "22", 1.7), ("22", "Buona_Vista", 1.5)]
red_edges_data = [("5", "4", 1.3), ("4", "3", 1.0), ("3", "2", 0.8), ("2", "Jurong_East", 1.4)]
orange_edges_data = [("23_orange", "Buona_Vista", 0.91), ("Buona_Vista", "21_orange", 0.91), ("21_orange", "20_orange", 1.5), ("20_orange", "Botanic_Gardens", 5.2),("Botanic_Gardens", "Caldecott", 3.9)]
blue_edges_data = [("8_blue", "Botanic_Gardens", 1.1), ("Botanic_Gardens", "Stevens", 1.3), ("Stevens", "11_blue", 1.7), ("11_blue", "12_blue", 1.4)]
brown_edges_data = [("Stevens", "12_brown", 1.8), ("12_brown", "13_brown", 0.93), ("13_brown", "14_brown", 1), ("14_brown", "15_brown", 1),("Stevens","Caldecott", 3)]

def add_edges_with_distance(edge_list):
    for u, v, km in edge_list:
        my_graph.add_edge(u, v, km=km, miles=round(km * 0.621371, 2))

add_edges_with_distance(green_edges_data)
add_edges_with_distance(red_edges_data)
add_edges_with_distance(orange_edges_data)
add_edges_with_distance(blue_edges_data)
add_edges_with_distance(brown_edges_data)

# 2. calculate positions based on distances and angles (km)
pos = {}
pos["Jurong_East"] = (3.0, 9.0)
def calculate_pos(ref_node, new_node, distance_km, angle_deg):
    x, y = pos[ref_node]
    angle_rad = np.radians(angle_deg) 
    
    # display distance on the graph: 1 km = 2.5 units (adjust as needed for better spacing)
    scale_factor = 2.5 
    
    pos[new_node] = (x + (distance_km * scale_factor) * np.cos(angle_rad), 
                     y + (distance_km * scale_factor) * np.sin(angle_rad))

# Run the calculate_pos functions 
calculate_pos("Jurong_East", "25", 1.5, 180)
calculate_pos("Jurong_East", "23", 3.5, 0)
calculate_pos("23", "22", 1.7, 0)
calculate_pos("22", "Buona_Vista", 1.5, 0)
calculate_pos("Jurong_East", "2", 1.6, 90)
calculate_pos("2", "3", 1.5, 90)
calculate_pos("3", "4", 1.5, 90)
calculate_pos("4", "5", 1.7, 90)
calculate_pos("Buona_Vista", "23_orange", 1.7, 265) 
calculate_pos("Buona_Vista", "21_orange", 1.7, 80)
calculate_pos("21_orange", "20_orange", 1.5, 60)
calculate_pos("20_orange", "Botanic_Gardens", 5.2, 30)
calculate_pos("Botanic_Gardens", "8_blue", 1.1, 180)
calculate_pos("Botanic_Gardens", "Stevens", 1.3, 0)
calculate_pos("Stevens", "11_blue", 1.7, -40)
calculate_pos("11_blue", "12_blue", 1.4, -40)
calculate_pos("Stevens","Caldecott", 3.9, 90)
calculate_pos("Stevens", "12_brown", 1.8, -90)
calculate_pos("12_brown", "13_brown", 1.7, -90)
calculate_pos("13_brown", "14_brown", 1.5, -90)
calculate_pos("14_brown", "15_brown", 1.5, -90)

# ==========================================
# 3. calculate statistics
# ==========================================
interchange_nodes = ["Jurong_East", "Buona_Vista", "Botanic_Gardens", "Stevens","Caldecott"]
distances_km = [d["km"] for _,_,d in my_graph.edges(data=True)]
total_stations = my_graph.number_of_nodes()
total_inchanges = len(interchange_nodes)
total_km = sum(distances_km)

# ==========================================
# 4. visualization
# ==========================================
# initiate figure and axis
fig, ax = plt.subplots(figsize=(16, 10))

ax.margins(0.15)

# draw edges with colors based on the line
nx.draw_networkx_edges(my_graph, pos, edgelist=[(u,v) for u,v,_ in green_edges_data], edge_color="green", width=4)
nx.draw_networkx_edges(my_graph, pos, edgelist=[(u,v) for u,v,_ in red_edges_data], edge_color="red", width=4)
nx.draw_networkx_edges(my_graph, pos, edgelist=[(u,v) for u,v,_ in orange_edges_data], edge_color="orange", width=4)
nx.draw_networkx_edges(my_graph, pos, edgelist=[(u,v) for u,v,_ in blue_edges_data], edge_color="blue", width=4)
nx.draw_networkx_edges(my_graph, pos, edgelist=[(u,v) for u,v,_ in brown_edges_data], edge_color="brown", width=4)

# draw nodes with colors based on the line and interchange status
normal_nodes = [n for n in my_graph.nodes if n not in interchange_nodes]
node_colors = []
for node in normal_nodes:
    if "orange" in node: node_colors.append("orange")
    elif "blue" in node: node_colors.append("blue")
    elif "brown" in node: node_colors.append("brown")
    elif node in ["25", "23", "22"]: node_colors.append("green")
    else: node_colors.append("red")

nx.draw_networkx_nodes(my_graph, pos, nodelist=normal_nodes, node_color=node_colors, node_size=350)
nx.draw_networkx_nodes(my_graph, pos, nodelist=interchange_nodes, node_color="#9b9b9b", node_size=350, edgecolors="black", linewidths=2)

# label nodes with short names (Short Labels)
short_labels = {n: ("" if n in interchange_nodes else n.split("_")[0]) for n in my_graph.nodes}
nx.draw_networkx_labels(my_graph, pos, labels=short_labels, font_size=8, font_color="white", font_weight="bold")

# Station Names
station_names = {
    "Jurong_East": "Jurong East", "25": "Chinese Garden", "23": "Clementi", "22": "Dover",
    "Buona_Vista": "Buona Vista", "2": "Bukit Batok", "3": "Bukit Gombak", "4": "Choa Chu Kang",
    "5": "Yew Tee", "23_orange": "One-North", "21_orange": "Holland Village", "20_orange": "Farrer Road",
    "Botanic_Gardens": "Botanic\nGardens", "8_blue": "Tan Kah Kee", "Stevens": "Stevens",
    "11_blue": "Newton", "12_blue": "Little India",
    "12_brown": "Mount Pleasant", "13_brown": "Napier", "14_brown": "Orchard Blvd", "15_brown": "Orchard",
    "Caldecott": "Caldecott" 
}


label_offsets = {
            # stations on the Green Line (Horizontal) -> 
    "25": (0, 1.5), "Jurong_East": (0, -1.2), "23": (0, -1.2), "22": (0, -1.2), "Buona_Vista": (2.7, 0),
    
    # stations on the Red Line (Vertical) 
    "2": (-2.7, 0), "3": (-3, 0), "4": (-3.2, 0), "5": (-2.2, 0),
    
    # stations on the Orange Line (Diagonal)
    "23_orange": (0, -1.2), "21_orange": (3.5, 0), "20_orange": (0, 1.2),
    
    # stations on the Blue Line (Horizontal/Diagonal)
    "8_blue": (0, 1.2), "11_blue": (2.0, 0), "12_blue": (2.5, 0),
    
    # stations on the Brown Line (Vertical)
    "12_brown": (-3.4, 0), "13_brown": (2.2, 0), "14_brown": (3.2, 0), "15_brown": (2.2, 0),
    
    # Interchange
    "Botanic_Gardens": (0, -1.6), 
    "Stevens": (2.2, 0.5),           
    "Caldecott": (-2.5, 0)           
}
label_pos = {node: (coords[0] + label_offsets.get(node, (0, 0.5))[0], coords[1] + label_offsets.get(node, (0, 0.5))[1]) for node, coords in pos.items()}
nx.draw_networkx_labels(my_graph, label_pos, labels=station_names, font_size=9, font_color="black", font_weight="bold")

# draw edge labels with distances (km or miles)
edge_labels = {(u,v): f"{my_graph[u][v][unit]}" for u,v in my_graph.edges()}
# update edge label drawing to include bbox for better readability
nx.draw_networkx_edge_labels(
    my_graph, 
    pos, 
    edge_labels=edge_labels, 
    font_size=8,
    font_weight="bold", 
    
    bbox=dict(
        facecolor='white',  
        edgecolor='none',   
        pad=2,              
        alpha=0.9           
    )
)

plt.axis("off")


# ==========================================
# LEGEND & STATISTICS PRINTING
# ==========================================

# Title
plt.title('System Map : MRT Singapore', fontsize=20, fontweight='bold', pad=20)

# create custom legend entries by plotting invisible lines and points with the same colors and labels as the actual graph elements
plt.plot([], [], color="green", linewidth=4, label="East-West Line")
plt.plot([], [], color="red", linewidth=4, label="North-South Line")
plt.plot([], [], color="orange", linewidth=4, label="Circle Line")
plt.plot([], [], color="blue", linewidth=4, label="Downtown Line")
plt.plot([], [], color="brown", linewidth=4, label="Thomson-East Coast")
plt.scatter([], [], color="#9b9b9b", edgecolor="black", s=150, label="Interchange")

# Display Legend: Use loc='upper center' and negative y to place the legend's top below the plot
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, 
           frameon=True, fontsize=12, title=f"Distance Unit: {unit.upper()}", title_fontsize=14)


# (Part Print statistics to console)
print("\n--- TASK 2: NETWORK STATISTICS ---")


distances_miles = [d["miles"] for _,_,d in my_graph.edges(data=True)]
total_miles = sum(distances_miles)
avg_km = np.mean(distances_km)
avg_miles = np.mean(distances_miles)

# 
stats_data = {
    "Metric": ["Total Length", "Average Distance"],
    "Kilometers (km)": [round(total_km, 2), round(avg_km, 2)],
    "Miles (miles)": [round(total_miles, 2), round(avg_miles, 2)]
}
df_stats = pd.DataFrame(stats_data)
print(df_stats.to_string(index=False))
print("-" * 35)
print(f"Total stations: {total_stations}")
print(f"Total interchanges: {total_inchanges}")

# Ví dụ tính toán cho từng line để in ra bảng
lines_info = {
    "East-West (Green)": green_edges_data,
    "North-South (Red)": red_edges_data,
    "Circle (Orange)": orange_edges_data,
    "Downtown (Blue)": blue_edges_data,
    "Thomson-East Coast (Brown)": brown_edges_data
}

detailed_stats = []
for name, data in lines_info.items():
    dist_list = [d[2] for d in data] # Lấy km
    dist_miles_list = [d[2] * 0.621371 for d in data] # Quy đổi ra miles

    detailed_stats.append({
        "Line": name,
        "Total Length": sum(dist_list),
        "Avg Distance": np.mean(dist_list),
        "Total Length (Miles)": sum(dist_miles_list),
        "Avg Distance (Miles)": np.mean(dist_miles_list)

    })

print("\n--- Detailed Line Statistics ---")
df_detailed = pd.DataFrame(detailed_stats)
print(df_detailed)


plt.subplots_adjust(bottom=0.25) 
plt.show()

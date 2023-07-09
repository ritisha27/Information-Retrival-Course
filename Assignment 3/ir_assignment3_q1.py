# -*- coding: utf-8 -*-
"""IR_Assignment3_Q1_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N4s_Ny26-SwL5fpvZ0ZfVyFvxXYMNLkL
"""

!wget 'https://snap.stanford.edu/data/p2p-Gnutella05.txt.gz'

!gunzip '/content/p2p-Gnutella05.txt.gz'

with open('/content/p2p-Gnutella05.txt', 'r') as file:
  data = file.read().splitlines(True)

with open('/content/p2p-Gnutella05.txt', 'w') as file:
    file.writelines(data[3:])

from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

df = pd.read_csv("/content/p2p-Gnutella05.txt", sep="\t")
df.rename(columns = {'# FromNodeId': 'FromNodeId'}, inplace = True)
df.head(10)

# Node with maximum Out-Degree
print(df['FromNodeId'].value_counts().max())
print(df['FromNodeId'].value_counts().idxmax())

# Node with maximum In-Degree
print(df['ToNodeId'].value_counts().max())
print(df['ToNodeId'].value_counts().idxmax())

# Create a mapping between the original node IDs and the zero-indexed consecutive node IDs
node_id_map = {}
node_id_counter = 0

for index, each_row in df.iterrows():
  src = each_row['FromNodeId']
  dest = each_row['ToNodeId']

  if src not in node_id_map:
    node_id_map[src] = node_id_counter
    node_id_counter += 1

  if dest not in node_id_map:
    node_id_map[dest] = node_id_counter
    node_id_counter += 1

#print(node_id_map)

"""### **Represent the network in terms of its adjacency matrix**"""

adj_matrix = np.zeros((len(node_id_map), len(node_id_map)))
for index, each_row in df.iterrows():
  src = each_row['FromNodeId']
  des = each_row['ToNodeId']
  src_mapping, dest_mapping = node_id_map[src], node_id_map[des]
  adj_matrix[src_mapping][dest_mapping] = 1

print(adj_matrix)

adj_matrix.shape

"""### **Represent the network in terms of its edge list.**"""

# Create the edge list
edges = []
for index, each_row in df.iterrows():
  src = each_row['FromNodeId']
  des = each_row['ToNodeId']
  edges.append((src, des))

#print(edges)

print(f'The count of Edges is {len(edges)}')

"""## **Briefly describe the dataset chosen and report the following:**

### **1. Number of Nodes**
"""

num_nodes = adj_matrix.shape[0]
print(f"Number of Nodes in the Network: {num_nodes}")

"""### **2. Number of Edges**"""

num_edges = int(np.sum(adj_matrix))
print(f"Number of Edges in the Network: {num_edges}")

"""### **3. Avg In-degree**"""

in_degrees = np.sum(adj_matrix, axis=0)
avg_in_degree = np.mean(in_degrees)
print(f"Average In-degree of the Network: {avg_in_degree}")

in_degrees

"""### **4. Avg Out-degree**"""

out_degrees = np.sum(adj_matrix, axis=1)
avg_out_degree = np.mean(out_degrees)
print(f"Average Out-degree of the Network: {avg_out_degree}")

"""### **5. Node with Max In-degree**"""

def get_key(val):
    for key, value in node_id_map.items():
        if val == value:
            return key
    return "Key doesn't exist"

# Get the ID for the maximum 
max_in_degree_node_index = np.argmax(in_degrees)

# Get the maximum degree value
print(f'The maximum value of In-Degree is as : {int(in_degrees[max_in_degree_node_index])}')

# Get the Actual Node - ID using the node_id_map
print(f'The Node-ID with maximum In-Degree is as: {get_key(max_in_degree_node_index)}')

"""### **6. Node with Max out-degree**"""

max_out_degree_node_index = np.argmax(out_degrees)

# Get the maximum degree value
print(f'The maximum value of Out-Degree is as : {int(out_degrees[max_out_degree_node_index])}')

# Get the Actual Node - ID using the node_id_map
print(f'The Node-ID with maximum Out-Degree is as: {get_key(max_out_degree_node_index)}')

"""### **7. The density of the network**"""

density = num_edges / (num_nodes * (num_nodes - 1))
print(f"Density of the Network: {density}")

"""## **Further, perform the following tasks:**

### **1. [5 points] Plot degree distribution of the network (in case of a directed graph, plot in-degree and out-degree separately).**

#### **In-Degree Distribution**
"""

# degree distribution
in_counter = Counter(list(in_degrees))
out_counter = Counter(list(out_degrees))

in_degrees.max()

if 457 in in_counter.keys():
  print('HI')

in_counter[457]

print(in_counter)

# Plotting the In-Degree Distribution
in_keys = list(in_counter.keys())
in_values = list(in_counter.values())
out_keys = list(out_counter.keys())
out_values = list(out_counter.values())
# df_values = pd.DataFrame(in_degrees)
# values = df_values.value_counts(normalize=True, sort=False)

# As the value are extremely low, plot a log based graph for distribution. Create a bar graph with a logarithmic y-axis
fig, ax = plt.subplots()
ax.bar(in_keys, in_values)
ax.set_yscale('log')
# Add Labels and Title
ax.set_xlabel('In-Degree')
ax.set_ylabel('Count - (log scale)')
ax.set_title('Bar-Plot for In-Degree Distribution of the network.')
plt.grid()
# Show the plot
plt.show()

# Create a histogram with 10 bins
fig, ax = plt.subplots()
#n, bins, patches = ax.hist(in_values, bins=1000)

# Add data points on top of the histogram2
ax.scatter(in_keys,in_values)
ax.set_yscale('log')
ax.set_xlim([0,100])
# Add labels and title
ax.set_xlabel('In-Degree')
ax.set_ylabel('Count')
ax.set_title('Scatter Plot for In-Degree Distribution')
plt.grid()
# Show the plot
plt.show()

fig, ax = plt.subplots()
ax.bar(out_keys, out_values)
ax.set_yscale('log')
# Add Labels and Title
ax.set_xlabel('Out-Degree')
ax.set_ylabel('Count - (log scale)')
ax.set_title('Plot for Out-Degree Distribution of the network.')
# Show the plot
plt.show()

# Create a histogram with 10 bins
fig, ax = plt.subplots()
#n, bins, patches = ax.hist(in_values, bins=1000)

# Add data points on top of the histogram2
ax.scatter(out_keys,out_values)
ax.set_yscale('log')
ax.set_xlim([0,100])
# Add labels and title
ax.set_xlabel('Out-Degree')
ax.set_ylabel('Count')
ax.set_title('Scatter Plot for Out-Degree Distribution')
plt.grid()
# Show the plot
plt.show()

"""### **2. [10 points] Calculate the local clustering coefficient of each node and plot the clustering-coefficient distribution (lcc vs frequency of lcc) of the network.**"""

# Calculate the local clustering coefficient of each node
lcc = np.zeros(num_nodes)
for node in range(num_nodes):
  neighbors = np.nonzero(adj_matrix[node])[0]  # Get the neighbors of the node
  num_neighbors = len(neighbors)
  if num_neighbors < 2:
    lcc[node] = 0  # If the node has less than two neighbors, its lcc is 0
  else:
    num_links = 0
    for i in range(num_neighbors):
      for j in range(i+1, num_neighbors):
        if adj_matrix[neighbors[i], neighbors[j]] == 1:
          num_links += 1

    lcc[node] = 2 * num_links / (num_neighbors * (num_neighbors - 1))

lcc_values, lcc_counts = np.unique(lcc, return_counts=True)

plt.scatter(lcc_values, lcc_counts)
plt.xlabel("Local Clustering Coefficient")
plt.ylabel("Frequency")
plt.title("Clustering-Coefficient Distribution")
plt.show()
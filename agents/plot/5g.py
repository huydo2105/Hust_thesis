# Import necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create a DataFrame for the data
data = {'Nodes': [ 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'A_TPS': [147,800,1200,1400,1835,1840,1850,1850,1850,1853],
        'B_TPS': [147 , 300, 350, 400, 500, 505, 510, 510, 510, 510],
        'C_TPS': [147 , 350, 400, 450, 500, 550, 600, 650, 700, 750],
        'A_Capacity': [160 , 100, 80, 65, 50, 45, 40, 37, 30, 26],
        'B_Capacity': [140 , 70, 46.67, 35, 28, 23.33, 20, 17.5, 15.5, 14],
        'C_Capacity': [120 , 65, 40, 32, 22, 18, 14, 11, 9, 8],
        'A_Latency': [40 , 30, 28, 25, 23, 20, 18, 16, 14, 12],
        'B_Latency': [70 , 60, 55, 50, 47, 45, 42, 40, 38, 35],
        'C_Latency': [50 , 40, 38, 35, 33, 30, 28, 26, 24, 22],
        'A_Utilization': [90 , 80, 78, 75, 73, 70, 68, 65, 63, 60],
        'C_Utilization': [60 , 50, 48, 45, 43, 40, 38, 35, 33, 30],
        'B_Utilization': [40 , 30, 28, 25, 23, 20, 18, 16, 14, 12]}

df = pd.DataFrame(data)

# Set up the first plot
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.lineplot(x='Nodes', y='A_TPS', data=df, ax=ax1, label='our platform')
sns.lineplot(x='Nodes', y='B_TPS', data=df, ax=ax1, label='equitable sharing of resource platform')
sns.lineplot(x='Nodes', y='C_TPS', data=df, ax=ax1, label='best effort platform')
ax1.set_ylabel('Throughput (TPS)')
ax1.set_xlabel('Network node')
plt.savefig('./figures/transaction_data.png')

# Set up the second plot
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.lineplot(x='Nodes', y='A_Latency', data=df, ax=ax2, label='our platform')
sns.lineplot(x='Nodes', y='B_Latency', data=df, ax=ax2, label='equitable sharing of resource platform')
sns.lineplot(x='Nodes', y='C_Latency', data=df, ax=ax2, label='best effort platform')
ax2.set_ylabel('Latency (ms)')
ax2.set_xlabel('Network node')
plt.savefig('./figures/latency_data.png')

# Set up the third plot
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.lineplot(x='Nodes', y='A_Utilization', data=df, ax=ax3, label='our platform')
sns.lineplot(x='Nodes', y='B_Utilization', data=df, ax=ax3, label='equitable sharing of resource platform')
sns.lineplot(x='Nodes', y='C_Utilization', data=df, ax=ax3, label='best effort platform')
ax3.set_ylabel('Utilization (%)')
ax3.set_xlabel('Network node')
plt.savefig('./figures/utiliation_data.png')

# Set up the fourth plot
fig1, ax4 = plt.subplots(figsize=(8, 4))
sns.lineplot(x='Nodes', y='A_Capacity', data=df, ax=ax4, label='our platform')
sns.lineplot(x='Nodes', y='B_Capacity', data=df, ax=ax4, label='equitable sharing of resource platform')
sns.lineplot(x='Nodes', y='C_Capacity', data=df, ax=ax4, label='best effort platform')
ax4.set_ylabel('Network capacity per node (Mbps)')
ax4.set_xlabel('Network node')
plt.savefig('./figures/capacity_data.png')

plt.show()
# This will create three separate plots, one for each of the three metrics, each with its own title and y-axis label.







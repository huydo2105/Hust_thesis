import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file into a pandas DataFrame
ddpg = pd.read_csv("/home/fetia/IdeaProjects/mkchain/data/run-DDPG_0-tag-rollout_ep_rew_mean.csv")
sac = pd.read_csv("/home/fetia/IdeaProjects/mkchain/data/run-SAC_0-tag-rollout_ep_rew_mean(1).csv")
tezos = []
tezos_tps = []

for i in range(len(ddpg)):
    ddpg["Value"][i] *= 5
for i in range(len(sac)):
    sac["Value"][i] *= 5
for i in range(1600):
    tezos.append(346)
for i in range(100):
    tezos_tps.append(346)

# Extract the Step and Value columns
ddpg_steps = ddpg["Step"]
ddpg_values = ddpg["Value"]
sac_steps = sac["Step"]
sac_values = sac["Value"]

# #plot 4: number of required nodes
# # Create plot
# shard_size = [3,10,20,30,40,50,60,70,80,90,100]
# tps = [147,500,800,1200,1400,1835,1840,1850,1850,1850,1853]

# plt.plot(shard_size, tps, label="Dynamic sharding-based blockchain")
# plt.xlabel('Shard size')
# plt.ylabel('Throughput (tps)')
# plt.plot(tezos_tps, color='y',label="Tezos blockchain")
# plt.legend()
# # Save the figure
# plt.savefig("./figures/ddpg_num_nodes.png")
# plt.show()

# # Plot the chart
# plt.plot(ddpg_steps, ddpg_values, label="Dynamic sharding-based blockchain")
# # Add a horizontal line at y=346
# plt.plot(tezos, color='y',label="Tezos blockchain")
# # Add a legend and axis labels
# plt.legend()
# plt.xlabel("Episodes")
# plt.ylabel("Throughput(TPS)")
# # save the figure
# plt.savefig("./figures/ddpg_tps.png")
# plt.show()

#plot 4: number of required nodes
# Create plot
shard_num = [1,2,3,4,5]
tps = [1853, 2400, 3000, 4500, 5200]

plt.plot(shard_num, tps, label="Dynamic sharding-based blockchain")
plt.xlabel('Number of shards')
plt.ylabel('Throughput (tps)')
# Set x-axis ticks with a step of 1
plt.xticks(range(min(shard_num), max(shard_num)+1, 1))
# Save the figure
plt.savefig("./figures/ddpg_num_shards.png")

plt.show()
# Plot balance and reward

fig, ax = plt.subplots()
# ax.set_ylabel('Reward')
# ax.set_xlabel('Episodes')
# ax.plot(env.reward_history, color='b')
# ax.tick_params(axis='y', labelcolor='b')

# # Highlight reward range
# reward_min = []
# reward_max = []
# for i in range(len(env.balance_history)):
#     reward_min.append(0.00005 * env.balance_history[i])
#     reward_max.append(0.0005 * env.balance_history[i])
# ax.fill_between(range(len(env.reward_history)), reward_min, reward_max, color='orange', alpha=0.3)

# fig.tight_layout()
# plt.show()
# # Save the figure
# fig.savefig("./figures/balance.png")
# plt.close(fig)

# Plot balance and reward

# fig, ax = plt.subplots()
# ax.set_ylabel('Punishment')
# ax.set_xlabel('Episodes')
# ax.plot(env.punishment_history, color='b')
# ax.tick_params(axis='y', labelcolor='b')

# # Highlight punishment range
# punishment_min = []
# punishment_max = []
# for i in range(len(env.balance_history)):
#     punishment_min.append(0.01 * env.balance_history[i])
#     punishment_max.append(0.3 * env.balance_history[i])
# ax.fill_between(range(len(env.punishment_history)), punishment_min, punishment_max, color='orange', alpha=0.3)

# fig.tight_layout()
# plt.show()
# # Save the figure
# fig.savefig("./figures/punishment.png")
# plt.close(fig)

# # Scatter plot 1: block size vs memory
# fig, ax = plt.subplots()
# ax.scatter(env.block_size_history, env.memory_history)

# # Add labels and title
# ax.set_xlabel('Block Size')
# ax.set_ylabel('Memory')
# ax.set_title('Block Size vs. Memory')
# colors = np.where(env.block_size_history > env.memory_history, 'r', 'b')

# plt.show()
# # Save the figure
# fig.savefig("./figures/ddpg_block_size_memory.png")
# plt.close(fig)

# # Scatter plot 2: block size vs cpu
# fig, ax = plt.subplots()
# ax.scatter(env.block_size_history, env.cpu_history)

# # Add labels and title
# ax.set_xlabel('Block Size')
# ax.set_ylabel('CPU')
# ax.set_title('Block Size vs. CPU')
# colors = np.where(env.block_size_history > env.cpu_history, 'r', 'b')

# plt.show()
# # Save the figure
# fig.savefig("./figures/ddpg_block_size_cpu.png")
# plt.close(fig)


# # plot 3: Requirement
# # Assign labels
# labels = ['Emmy+' if x == 0 else 'Tenderbake' for x in env.requirement_history]
# print(env.requirement_history)
# env.requirement_history[0] = 0
# # Create plot
# plt.plot(env.requirement_history)
# plt.xlabel('Episodes')
# plt.ylabel('Requirement')

# plt.show()
# # # Save the figure
# fig.savefig("./figures/ddpg_requirement.png")
# plt.close(fig)

# #plot 4: number of required nodes
# # Create plot
# shard_size = [3,10,20,30,40,50,60,70,80,90,100]
# tps = [69,175,255,268,382,390,582,830,852,862,862]
# print(env.tps_history)
# plt.plot(shard_size, env.tps)
# plt.xlabel('Shard size')
# plt.ylabel('Throughput (tps)')


# plt.show()
# # # Save the figure
# fig.savefig("./figures/ddpg_num_nodes.png")
# plt.close(fig)

# #plot 5: block size

# # Create plot
# plt.plot(env.block_size_history)
# plt.xlabel('Episodes')
# plt.ylabel('Block size(B)')

# plt.show()
# # # Save the figure
# fig.savefig("./figures/ddpg_block_size.png")
# plt.close(fig)

# #plot 4: tps
# # Create plot
# for i in range(len(env.tps_history)):
#     env.tps_history[i] *= 1
# plt.plot(env.tps_history)
# plt.xlabel('Episode')
# plt.ylabel('Throughput (tps)')
# plt.show()
# fig.savefig("./figures/ddpg_tps1.png")
# plt.close(fig)


 #plot 4: malicious nodes
# ax.set_ylabel('Shard size')
# ax.set_xlabel('Episodes')
# ax.plot(env.malicious_nodes_history, color='b')
# ax.tick_params(axis='y', labelcolor='b')

# Highlight punishment range
# malicous_nodes_min = []
# malicous_nodes_max = []
# for i in range(len(env.num_nodes_history)):
#     malicous_nodes_min.append(0)
#     malicous_nodes_max.append(int(1/3 * env.num_nodes_history[i]))
# ax.fill_between(range(len(env.malicious_nodes_history)), malicous_nodes_min, malicous_nodes_max, color='orange', alpha=0.3)
# plt.show()
print(env.block_size_history)
fig.savefig("./figures/ddpg_malicious.png")
plt.close(fig)
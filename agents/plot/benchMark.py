import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create a DataFrame for the data
avg_txs = {
    'size': [50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
    'ours': [2000, 1050, 600, 500, 400, 350, 300, 250, 200, 140],
    'fixed_consensus': [1400, 750, 450, 420, 350, 300, 250, 200, 150, 60],
    'fixed_block_size': [1200, 600, 400, 350, 320, 280, 230, 180, 100, 45],
}

num_nodes = {
    'size': [10, 50, 100, 150, 200, 250, 300],
    'ours': [140, 680, 880, 1000, 1150, 1180, 1200],
    'fixed_consensus': [120, 350, 600, 780, 800, 840, 880],
    'fixed_block_size': [60, 60, 61, 60, 61, 62, 62],
}

df = pd.DataFrame(avg_txs)
df1 = pd.DataFrame(num_nodes)
# Set up the first plot
fig1, ax1 = plt.subplots(figsize=(8, 4))

# Add a smoothed curve to the ours line
sns.lineplot(x='size', y='ours', data=df, ax=ax1, label='our platform', color='#377eb8', linewidth=3, alpha=0.7)

# Add a smoothed curve to the fixed_consensus line
sns.lineplot(x='size', y='fixed_consensus', data=df, ax=ax1, label='fixed consensus algorithm', color='#ff7f00', linewidth=3, alpha=0.7)

# Add a smoothed curve to the fixed_block_size line
sns.lineplot(x='size', y='fixed_block_size', data=df, ax=ax1, label='fixed block size', color='#98df8a', linewidth=3, alpha=0.7)

# Add a point marker to each data point
for i in range(len(df)):
    ax1.plot(df['size'][i], df['ours'][i], 'o', color='#377eb8', alpha=0.7)
    ax1.plot(df['size'][i], df['fixed_consensus'][i], 'o', color='#ff7f00', alpha=0.7)
    ax1.plot(df['size'][i], df['fixed_block_size'][i], 'o', color='#98df8a', alpha=0.7)

# Add a title and labels to the axes
ax1.set_ylabel('Throughput (TPS)')
ax1.set_xlabel('Average Transaction Size (B)')

# Add a legend
ax1.legend()

# Save the figure
plt.savefig('../figures/transaction_size.png')


fig2, ax2 = plt.subplots(figsize=(8, 4))

# Add a smoothed curve to the ours line
sns.lineplot(x='size', y='ours', data=df, ax=ax2, label='our platform', color='#377eb8', linewidth=3, alpha=0.7)

# Add a smoothed curve to the fixed_consensus line
sns.lineplot(x='size', y='fixed_consensus', data=df, ax=ax2, label='fixed consensus algorithm', color='#ff7f00', linewidth=3, alpha=0.7)

# Add a smoothed curve to the fixed_block_size line
sns.lineplot(x='size', y='fixed_block_size', data=df, ax=ax2, label='fixed block size', color='#98df8a', linewidth=3, alpha=0.7)

# Add a point marker to each data point
for i in range(len(df)):
    ax2.plot(df['size'][i], df['ours'][i], 'o', color='#377eb8', alpha=0.7)
    ax2.plot(df['size'][i], df['fixed_consensus'][i], 'o', color='#ff7f00', alpha=0.7)
    ax2.plot(df['size'][i], df['fixed_block_size'][i], 'o', color='#98df8a', alpha=0.7)

# Add a title and labels to the axes
ax2.set_ylabel('Throughput (TPS)')
ax2.set_xlabel('Average Transaction Size (B)')

# Add a legend
ax2.legend()

# Save the figure
plt.savefig('../figures/transaction_size.png')

plt.show()

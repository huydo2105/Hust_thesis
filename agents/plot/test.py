import matplotlib.pyplot as plt

# Define the requirement list
requirement = [0, 1]

# Set the tick labels on y-axis
plt.yticks(requirement, ["Emmyplus", "Tenderbake"])

# Set the axis labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Requirement")

# Show the plot
plt.show()
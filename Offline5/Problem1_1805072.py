import numpy as np

ITERATION = 10000
probabilities = np.zeros((10, 5))

def fission():
    # Calculate individual probabilities
    p1 = 0.2126
    p2 = 0.2126 * 0.5893
    p3 = 0.2126 * 0.5893**2
    p0 = 1 - p1 - p2 - p3
    return min(np.random.choice([0, 1, 2, 3], p=[p0, p1, p2, p3]), 4)

# Simulation loop
for _ in range(ITERATION):
    # Initialize prev and next_neutrons for each iteration
    prev = 1
    next_neutrons = 0
    for generation in range(10):
        while prev != 0:
            prev -= 1
            next_neutrons += fission()

        # Counting neutrons for this generation
        if next_neutrons <= 3:
            probabilities[generation][next_neutrons] += 1  
        
        # Reset prev and next_neutrons for the next generation
        prev = next_neutrons
        next_neutrons = 0

# Normalize the probabilities
probabilities /= ITERATION

# Write probabilities to file
with open('problem1_output.txt', 'w') as file:
    for generation in range(10):
        file.write(f'\nGeneration-{generation + 1}:\n')
        for num_neutrons, prob in enumerate(probabilities[generation]):
            file.write(f'p[{num_neutrons}] = {prob:.4f}\n')

import math

# Constants for PMMLCG
MODLUS = 2147483647
MULT1 = 24112
MULT2 = 26143

# Default seeds
zrng = [1973272912, 281629770, 20006270]

# PMMLCG implementation
def lcgrand(stream):
    zi, lowprd, hi31 = zrng[stream], 0, 0
    lowprd = (zi & 65535) * MULT1
    hi31 = (zi >> 16) * MULT1 + (lowprd >> 16)
    zi = ((lowprd & 65535) - MODLUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
    if zi < 0:
        zi += MODLUS
        lowprd = (zi & 65535) * MULT2
        hi31 = (zi >> 16) * MULT2 + (lowprd >> 16)
        zi = ((lowprd & 65535) - MODLUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
    if zi < 0:
        zi += MODLUS
    zrng[stream] = zi
    return (zi >> 7 | 1) / 16777216.0

# Read input parameters from 'in.txt'
with open('in.txt', 'r') as file:
    A, S, N = map(float, file.readline().split())  # Mean inter-arrival time, mean service time, total number of delays

# Initialize simulation variables
clock = 0.0
num_customers = 0
total_delay = 0.0
num_delayed = 0
mean_inter_arrival_time = A
mean_service_time = S
total_delays = int(N)

# Function to handle a single time step of the simulation
def simulation_step():
    global clock, num_customers, total_delay, num_delayed
    arrival_time = -mean_inter_arrival_time * math.log(lcgrand(1))
    service_time = -mean_service_time * math.log(lcgrand(2))

    if arrival_time < service_time:
        clock = arrival_time
        num_customers += 1
        if num_customers == 1:
            service_time = clock + (-mean_service_time * math.log(lcgrand(3)))
        with open("event_orders.txt", "a") as event_orders_file:
            event_orders_file.write(f"{num_delayed + 1}. Next event: Customer {num_customers} Arrival\n")
    else:
        clock = service_time
        num_customers -= 1
        if num_customers > 0:
            total_delay += clock
            num_delayed += 1
            service_time = clock + (-mean_service_time * math.log(lcgrand(3)))
            with open("event_orders.txt", "a") as event_orders_file:
                event_orders_file.write(f"{num_delayed}. Next event: Customer {num_customers + 1} Departure\n")
                event_orders_file.write(f"---------No. of customers delayed: {num_delayed}--------\n")
        else:
            service_time = float('inf')

# Function to run the simulation until N customers have been served
def run_simulation():
    global clock, num_customers, total_delay, num_delayed
    while num_delayed < total_delays:
        simulation_step()

    avg_delay = total_delay / total_delays
    avg_num_in_queue = total_delay / clock
    server_utilization = (total_delay + (mean_service_time * num_customers)) / clock
    end_time = clock

    with open("results.txt", "w") as results_file:
        results_file.write("----Single-Server Queueing System----\n")
        results_file.write(f"Mean inter-arrival time: {mean_inter_arrival_time:.6f} minutes\n")
        results_file.write(f"Mean service time: {mean_service_time:.6f} minutes\n")
        results_file.write(f"Number of customers: {total_delays}\n\n")
        
        results_file.write(f"Avg delay in queue: {avg_delay:.6f} minutes\n")
        results_file.write(f"Avg number in queue: {avg_num_in_queue:.6f}\n")
        results_file.write(f"Server utilization: {server_utilization:.6f}\n")
        results_file.write(f"Time simulation ended: {end_time:.6f} minutes\n")

# Run the simulation
run_simulation()

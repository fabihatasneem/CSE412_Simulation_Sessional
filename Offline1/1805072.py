import math
import sys

# File handling
infile = open("IOs/io2/in.txt", "r")
resultfile = open("results.txt", "w")
eventfile = open("event_orders.txt", "w")

# Constants for lcgrand
MODULUS = 2147483647
MULT1 = 24112
MULT2 = 26143
zrng = [1,
 1973272912, 281629770,  20006270,1280689831,2096730329,1933576050,
  913566091, 246780520,1363774876, 604901985,1511192140,1259851944,
  824064364, 150493284, 242708531,  75253171,1964472944,1202299975,
  233217322,1911216000, 726370533, 403498145, 993232223,1103205531,
  762430696,1922803170,1385516923,  76271663, 413682397, 726466604,
  336157058,1432650381,1120463904, 595778810, 877722890,1046574445,
   68911991,2088367019, 748545416, 622401386,2122378830, 640690903,
 1774806513,2132545692,2079249579,  78130110, 852776735,1187867272,
 1351423507,1645973084,1997049139, 922510944,2045512870, 898585771,
  243649545,1004818771, 773686062, 403188473, 372279877,1901633463,
  498067494,2087759558, 493157915, 597104727,1530940798,1814496276,
  536444882,1663153658, 855503735,  67784357,1432404475, 619691088,
  119025595, 880802310, 176192644,1116780070, 277854671,1366580350,
 1142483975,2026948561,1053920743, 786262391,1792203830,1494667770,
 1923011392,1433700034,1244184613,1147297105, 539712780,1545929719,
  190641742,1645390429, 264907697, 620389253,1502074852, 927711160,
  364849192,2049576050, 638580085, 547070247 ]
def lcgrand(seed):
    zi = zrng[seed]
    lowprd = (zi & 65535) * MULT1
    hi31 = (zi >> 16) * MULT1 + (lowprd >> 16)
    zi = ((lowprd & 65535) - MODULUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
    if zi < 0:
        zi += MODULUS
    lowprd = (zi & 65535) * MULT2
    hi31 = (zi >> 16) * MULT2 + (lowprd >> 16)
    zi = ((lowprd & 65535) - MODULUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
    if zi < 0:
        zi += MODULUS
    zrng[seed] = zi
    return (zi >> 7 | 1) / 16777216.0

# Constants for queueing system
Q_LIMIT = 100
BUSY = 1
IDLE = 0

# Simulation variables
next_event_type = 0
num_customers_delayed = 0
num_delays_required = 0
num_events = 2
num_in_q = 0
server_status = IDLE
area_num_in_q = 0.0
area_server_status = 0.0
mean_interarrival = 0.0
mean_service = 0.0
simulation_time = 0.0
time_arrival = [0.0] * (Q_LIMIT + 1)
time_last_event = 0.0
time_next_event = [0.0] * 3
total_of_delays = 0.0
event_count = 0

# Initialize function
def initialize():
    global simulation_time, server_status, num_in_q, time_last_event, num_customers_delayed, total_of_delays, area_num_in_q, area_server_status
    simulation_time = 0
    server_status = IDLE
    num_in_q = 0
    time_last_event = 0.0
    num_customers_delayed = 0
    total_of_delays = 0.0
    area_num_in_q = 0.0
    area_server_status = 0.0
    time_next_event[1] = simulation_time + expon(mean_interarrival)
    time_next_event[2] = sys.float_info.max

# Timing function
def timing():
    global next_event_type, simulation_time
    min_time_next_event = sys.float_info.max
    next_event_type = 0

    for i in range(1, num_events + 1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i

    if next_event_type == 0:
        print(f"\nEvent list is empty at time {simulation_time}")
        sys.exit(1)
    
    simulation_time = min_time_next_event

# Arrival event function
def arrive():
    global simulation_time, server_status, num_in_q, total_of_delays, num_customers_delayed, event_count
    time_next_event[1] = simulation_time + expon(mean_interarrival)
    event_count += 1
    eventfile.write(f"{event_count}. Next event: Customer {num_customers_delayed + 1} Arrival\n") 

    if server_status == BUSY:
        num_in_q += 1
        if num_in_q > Q_LIMIT:
            print(f"\nOverflow of the array time_arrival at time {simulation_time}")
            sys.exit(2)
        time_arrival[num_in_q] = simulation_time
    else:
        delay = 0.0
        total_of_delays += delay
        num_customers_delayed += 1
        server_status = BUSY
        time_next_event[2] = simulation_time + expon(mean_service)
  
        eventfile.write(f"\n---------No. of customers delayed: {num_customers_delayed}--------\n\n")

# Departure event function
def depart():
    global simulation_time, server_status, num_in_q, total_of_delays, num_customers_delayed, event_count
    event_count += 1
    eventfile.write(f"{event_count}. Next event: Customer {num_customers_delayed} Departure\n")
    if num_in_q == 0:
        server_status = IDLE
        time_next_event[2] = sys.float_info.max
    else:
        num_in_q -= 1
        delay = simulation_time - time_arrival[1]
        total_of_delays += delay
        num_customers_delayed += 1
        time_next_event[2] = simulation_time + expon(mean_service)
        for i in range(1, num_in_q + 1):
            time_arrival[i] = time_arrival[i + 1]

        eventfile.write(f"\n---------No. of customers delayed: {num_customers_delayed}--------\n\n")

# Report generator function
def report():
    global total_of_delays, num_customers_delayed, area_num_in_q, simulation_time, area_server_status
    resultfile.write(f"\nAvg delay in queue: {total_of_delays / num_customers_delayed:.7f} minutes\n")
    resultfile.write(f"Avg number in queue: {area_num_in_q / simulation_time:.7f}\n")
    resultfile.write(f"Server utilization: {area_server_status / simulation_time:.7f}\n")
    resultfile.write(f"Time simulation ended: {simulation_time:.7f} minutes")

# Update area accumulators for time-average statistics
def update_time_avg_stats():
    global time_last_event, simulation_time, area_num_in_q, area_server_status
    time_since_last_event = simulation_time - time_last_event
    time_last_event = simulation_time
    area_num_in_q += num_in_q * time_since_last_event
    area_server_status += server_status * time_since_last_event

# Exponential variate generation function
def expon(mean):
    return -mean * math.log(lcgrand(1))

# Main simulation loop
mean_interarrival, mean_service, num_delays_required = map(float, infile.readline().split())
resultfile.write("----Single-Server Queueing System----\n\n")
resultfile.write(f"Mean inter-arrival time: {mean_interarrival:.7f} minutes\n")
resultfile.write(f"Mean service time: {mean_service:.7f} minutes\n")
resultfile.write(f"Number of customers: {int(num_delays_required)}\n")
initialize()
while num_customers_delayed < num_delays_required:
    timing()
    update_time_avg_stats()
    if next_event_type == 1:
        arrive()
    elif next_event_type == 2:
        depart()
report()
infile.close()
resultfile.close()
eventfile.close()
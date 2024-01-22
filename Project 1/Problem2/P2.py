import random
import math

def generate_exponential(lambda_):
    u = random.random()
    return -math.log(1 - u) / lambda_

def simulate_server_failure_and_restoration(total_hours):
    lambda_ = 1/500.0
    curr_time = 0
    failure_times = []
    restoration_times = []

    while curr_time < total_hours:
        uptime = generate_exponential(lambda_)
        curr_time += uptime
        if curr_time < total_hours:
            failure_times.append(curr_time)
            curr_time += 10
            restoration_times.append(curr_time)

    return failure_times, restoration_times

def check_system_failure(failure_times_1, restoration_times_1, failure_times_2, restoration_times_2):
    for f1, r1 in zip(failure_times_1, restoration_times_1):
        for f2, r2 in zip(failure_times_2, restoration_times_2):
            if f1 < r2 and f2 < r1:  
                return True, f1 if f1 > f2 else f2
    return False, None

# Sim for 20 years
total_hours = 20 * 365 * 24
failure_times_1, restoration_times_1 = simulate_server_failure_and_restoration(total_hours)
failure_times_2, restoration_times_2 = simulate_server_failure_and_restoration(total_hours)

# Print failure and restoration times
print("\t\t\t\tServer 1\t\t\t\t\t\tServer 2")
print("\t\t", "-"*40, "\t\t", "-"*40)
print("\t\tFailure Time\t\tRestoration Time\t\tFailure Time\t\tRestoration Time")
for f1, r1, f2, r2 in zip(failure_times_1, restoration_times_1, failure_times_2, restoration_times_2):
    print(f"{f1:23.2f}    {r1:26.2f}    {f2:23.2f}    {r2:26.2f}")

# Simulate and determine system failures
num_trials = 100
total_failure_times = []

for i in range(num_trials):
    random.seed(i)  # Setting a different seed for each simulation
    failure_times_1, restoration_times_1 = simulate_server_failure_and_restoration(total_hours)
    failure_times_2, restoration_times_2 = simulate_server_failure_and_restoration(total_hours)
    
    has_failed, failure_time = check_system_failure(failure_times_1, restoration_times_1, failure_times_2, restoration_times_2)
    
    if has_failed:
        total_failure_times.append(failure_time)

# Calc average failure time
average_failure_time = sum(total_failure_times) / len(total_failure_times) if total_failure_times else None
print(f"Average time until system failure: {average_failure_time:.2f} hours")

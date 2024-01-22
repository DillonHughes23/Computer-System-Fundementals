
import random
import math

class Process:
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_time = None
        self.finish_time = None

class Event:
    def __init__(self, time, event_type, process=None):
        self.time = time
        self.event_type = event_type
        self.process = process
        self.next = None

class EventQueue:
    def __init__(self):
        self.head = None
        self.size = 0  # Keep track of the size of the linked list

    def is_empty(self):
        return self.head is None

    def add_event(self, event):
        self.size += 1
        if self.is_empty() or event.time < self.head.time:
            event.next = self.head
            self.head = event
        else:
            current = self.head
            while current.next is not None and current.next.time < event.time:
                current = current.next
            event.next = current.next
            current.next = event

    def pop_event(self):
        if self.is_empty():
            return None
        self.size -= 1
        event = self.head
        self.head = event.next
        return event

    def __len__(self):
        return self.size


def generate_exponential_random_number(rate):
    p = random.uniform(0, 1)
    return -1 / rate * math.log(1 - p)

def generate_interarrival_time(rate):
    return generate_exponential_random_number(rate)

def generate_service_time(average_service_time):
    return generate_exponential_random_number(1 / average_service_time)

def run_simulation(average_arrival_rate, average_service_time):
    clock = 0
    next_arrival_time = generate_interarrival_time(average_arrival_rate)
    event_queue = EventQueue()
    event_queue.add_event(Event(next_arrival_time, 'arrival'))
    cpu_busy = False
    number_of_processes_completed = 0
    total_turnaround_time = 0
    total_cpu_busy_time = 0
    total_processes_in_ready_queue = 0
    last_event_time = 0
    
    while number_of_processes_completed < 10000:
        current_event = event_queue.pop_event()
        clock = current_event.time
        if current_event.event_type == 'arrival':
            service_time = generate_service_time(average_service_time)
            new_process = Process(clock, service_time)
            if not cpu_busy:
                cpu_busy = True
                new_process.start_time = clock
                new_process.finish_time = clock + service_time
                total_cpu_busy_time += service_time
                event_queue.add_event(Event(new_process.finish_time, 'departure', new_process))
            else:
                total_processes_in_ready_queue += (clock - last_event_time) * (len(event_queue) + 1)
            next_arrival = clock + generate_interarrival_time(average_arrival_rate)
            event_queue.add_event(Event(next_arrival, 'arrival'))
        elif current_event.event_type == 'departure':
            cpu_busy = False
            total_turnaround_time += (clock - current_event.process.arrival_time)
            number_of_processes_completed += 1
            if not event_queue.is_empty() and event_queue.head.event_type == 'arrival':
                cpu_busy = True
                next_process = Process(clock, generate_service_time(average_service_time))
                next_process.start_time = clock
                next_process.finish_time = clock + next_process.service_time
                total_cpu_busy_time += next_process.service_time
                event_queue.add_event(Event(next_process.finish_time, 'departure', next_process))
        last_event_time = clock
    
    average_turnaround_time = total_turnaround_time / 10000
    total_throughput = number_of_processes_completed / clock
    average_cpu_utilization = total_cpu_busy_time / clock
    average_processes_in_ready_queue = total_processes_in_ready_queue / clock
    return average_turnaround_time, total_throughput, average_cpu_utilization, average_processes_in_ready_queue

def simulator_run(average_arrival_rate, average_service_time):
    with open('simulation_results.txt', 'a') as f:  
        results = run_simulation(average_arrival_rate, average_service_time)
        output = (
            f"Arrival Rate: {average_arrival_rate}\n"
            f"Average Turnaround Time: {results[0]}\n"
            f"Total Throughput: {results[1]} processes per second\n"
            f"Average CPU Utilization: {results[2] * 100}%\n"
            f"Average Number of Processes in Ready Queue: {results[3]}\n"
        )
        f.write(output)
        f.write('\n' + '-'*50 + '\n\n')
        print(output)

def main():
    average_service_time = 0.04
    for average_arrival_rate in range(10, 31):
        simulator_run(average_arrival_rate, average_service_time)

if __name__ == "__main__":
    main()

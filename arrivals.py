import random
from datetime import datetime, timedelta

num_participants = 1000
start_time = 8.0  # 8:00 am
end_time = 18.0  # 6:00 pm
arrivals_per_minute_before_10 = 30  # Desired arrivals per minute before 10 am
arrivals_per_minute_after_4 = 30   # Desired arrivals per minute after 4 pm

def simulate_arrivals(num_participants, start_time, end_time, arrivals_per_minute_before_10, arrivals_per_minute_after_4):
    arrivals = []

    start_datetime = datetime(2024, 1, 1, int(start_time), 0)
    end_datetime = datetime(2024, 1, 1, int(end_time), 0)

    for _ in range(num_participants):
        time_difference = random.uniform(0, (end_datetime - start_datetime).total_seconds())
        arrival_datetime = start_datetime + timedelta(seconds=time_difference)

        # Calculate arrival rate based on desired number of arrivals per minute
        if arrival_datetime.time() < datetime(2024, 1, 1, 10, 0).time():
            arrival_rate = arrivals_per_minute_before_10 / 60.0
        elif arrival_datetime.time() > datetime(2024, 1, 1, 16, 0).time():
            arrival_rate = arrivals_per_minute_after_4 / 60.0
        else:
            arrival_rate = 0.3  # Default rate for other times

        if random.uniform(0, 1) < arrival_rate:
            arrivals.append(arrival_datetime)

    return sorted(arrivals)


arrivals = simulate_arrivals(num_participants, start_time, end_time, arrivals_per_minute_before_10, arrivals_per_minute_after_4)

print("Arrival times:")
for arrival in arrivals:
    print(arrival.strftime('%Y-%m-%d %H:%M:%S'))


#check for differences
ten = []
four = []
between = []

for arrival in arrivals:
    arrival_datetime = datetime.strptime(arrival.strftime("%H:%M"), "%H:%M")

    if arrival_datetime < datetime.strptime("10:00", "%H:%M"):
        ten.append(arrival_datetime)
    elif arrival_datetime > datetime.strptime("16:00", "%H:%M"):
        four.append(arrival_datetime)
    else:
        between.append(arrival_datetime)

print("Before 10 am:", len(ten))
print("After 4 pm:", len(four))
print("Between 10 am and 4 pm:", len(between))
print("_________________________________")
print("Before 10 am per hour:", len(ten)/2)
print("After 4 pm per hour:", len(four)/2)
print("Between 10 am and 4 pm:", len(between)/6)



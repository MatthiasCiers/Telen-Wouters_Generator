from datetime import time


'''
intervals = []
# Adjust these weight values as needed
low_weight = 1
high_weight = 2

for hour in range(24):
    for minute in [0, 30]:
        start_time = time(hour, minute, 0)
        # Adjusting end time for half-hour intervals and the last interval of the day
        if minute == 30 and hour == 23:  # Handle the last half-hour interval
            end_time = time(23, 59, 59)
        elif minute == 30:  # End time for half-hour intervals not at the end of the hour
            end_time = time(hour + 1, 0, 0)
        else:  # End time for the first half-hour interval of the hour
            end_time = time(hour, 29, 59)

        # Assigning weights: intervals before 01:30 get a low weight, intervals between 01:30 and 19:30 get a high weight
        if ((hour == 1 and minute == 0) or hour < 1 or hour > 19 or (hour == 19 and minute == 30)):
            weight = low_weight
        else:
            weight = high_weight

        intervals.append((start_time, end_time, weight))

# Normalize the weights to ensure they sum to 1
total_weight = sum(interval[2] for interval in intervals)
normalized_intervals = [(start, end, weight / total_weight) for start, end, weight in intervals]

# This will print each interval with its normalized start time, end time, and weight
for interval in normalized_intervals:
    print(interval)
'''
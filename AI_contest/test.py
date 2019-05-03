

from time import time
start_time = time()

for i in range(1000000):
    for j in range(100):
        continue

end_time = time()
time_taken = end_time - start_time # time_taken is in seconds

hours, rest = divmod(time_taken,3600)
minutes, seconds = divmod(rest, 60)

if seconds > 2:
    print("Yes")

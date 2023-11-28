import time 
time.sleep(1)
start = time.perf_counter()
time.sleep(4)
end = time.perf_counter()
print(end - start)
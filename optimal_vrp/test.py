import time

# get the start time
st = time.time()
print(st)
# main program
# find sum to first 1 million numbers
sum_x = 0
for i in range(10000001):
    sum_x += i

# wait for 3 seconds
time.sleep(3)
print('Sum of first 1 million numbers is:', sum_x)

# get the end time
et = time.time()
print(et)
# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
# Rules

# if a warmer day is j and normal day is i then output[i] = j - i
# warmer means strictly greater temperature, equal temp = 0 count
# if no warmer day exist = 0
# output array is the same as input array
# Daily Temperatures

# You are given an array of integers temperatures where temperatures[i] represents the daily temperatures on the ith day.

# Return an array where output[i] is the number of days after the ith day before a warmer temperature appears on a future day. If there is no day in the future where a warmer temperature will appear for the ith day, set output[i] to 0 instead.

# Examples
# ```python
# daily_temperatures([30,38,30,36,35,40,28])
# output = [1,4,1,2,1,0,0]

# daily_temperatures([22,21,20])
# output = [0,0,0]

# daily_temperatures([30,38,30,36,35,40,28])
# output = [1,4,1,2,1,0,0]```



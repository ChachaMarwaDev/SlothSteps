def binary_search(arr, target):
    left_array = 0
    right_array = len(arr) - 1

    while left_array <= right_array:
        mid_array = (right_array + left_array) // 2

        if arr[mid_array] == target:
            return mid_array
        
        elif arr[mid_array] > target:
            right_array = mid_array - 1

        else:
            left_array = mid_array + 1

    return None
    
my_array = [1, 2, 3, 5, 6, 7, 9]

print(binary_search(my_array, 9))


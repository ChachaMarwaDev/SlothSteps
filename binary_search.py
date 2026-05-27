def binary_search(arr, target):
    left_element = 0
    right_element = len(arr) - 1

    while left_element <= right_element:
        mid_element = (right_element + left_element) // 2

        if arr[mid_element] == target:
            return mid_element
        
        elif arr[mid_element] > target:
            right_element = mid_element - 1

        else:
            left_element = mid_element + 1

    return None
    
my_list = [1, 2, 3, 5, 6, 7, 9]

print(binary_search(my_list, 9))


def binary_search(arr, target):
    # Start with the full range of the sorted list.
    left_element = 0
    right_element = len(arr) - 1

    # Keep searching while the range is valid.
    while left_element <= right_element:
        # Pick the middle index of the current range.
        mid_element = (right_element + left_element) // 2

        # If the middle value is the target, return its position.
        if arr[mid_element] == target:
            return mid_element
        # If the target is smaller, narrow to the left half.
        elif arr[mid_element] > target:
            right_element = mid_element - 1
        # Otherwise narrow to the right half.
        else:
            left_element = mid_element + 1

    # If we exit the loop, the target was not found.
    return None

# Example usage: find the number 9 in a sorted list.
my_list = [1, 2, 3, 5, 6, 7, 9]
print(binary_search(my_list, 9))


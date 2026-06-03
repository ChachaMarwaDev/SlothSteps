test_list = [1, 2, 3, 5, 6, 7, 9] 
# no. of items = 7

def binary_search(test_list, target):
    if not test_list:
        return None
    
    mid = len(test_list) // 2

    if test_list[mid] == target:
        return test_list[mid]
    elif target < test_list[mid]:
        return binary_search(test_list[:mid], target)
    else:
        return binary_search(test_list[mid + 1:], target)



print(binary_search(test_list, 2))



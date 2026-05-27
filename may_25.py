# Quiz 1: write a recursive function to count number of items in a list
# Quiz 2: write a recursive function to find the maximum number in a list
# Quiz 3: come up with a recursive case and a base case for binary search

test_list = [1, 3, 4, 5, 6, 9, 15]

"""
Quiz 1:
A recursive function has to find how many items we have
I need to specify the base case and recursive case
"""
def number_of_items(test_list):
    # define our base case
    if len(test_list) == 0:
        return 0
    else:
        return 1 + number_of_items(test_list[1:])

print(number_of_items(test_list))
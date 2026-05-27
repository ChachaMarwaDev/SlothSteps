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
    for item in test_list:
        if item == 0:
            item += 1
            print(item)


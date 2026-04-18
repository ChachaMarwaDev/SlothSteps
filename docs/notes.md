April 12 - Solved the work with bruteforce, its now to the new solution.

### Lists 101
Lists
    1. are ordered
    2. are changeable
    3. allows duplication
    4. holds different data type
    
> List begin counting at 0 - infinity

syntax
```python
list_name = ["Item1", "Item2"] # How to declare a list


list_length = len(list_name) # a view of the list items

# Accessing elements
list_ranging = list_name[2:5] # 5 not included
list_ranging = list_name[-4:-1] # -1 not included

# Modifying lists
list_name.insert(1, "Item3")
list_name.append(1, "Item3")
list_name.extend(1, "Item3")
list_name.pop(1)
list_name.remove("Item3")
del list_name[1]

# Iterating lists
for i, value in enumerate(list_name): # for key, value pairs
    print(f"{i}:{value}")

for i in list_name:
    print(i)


```
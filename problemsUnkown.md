🔢 Array Update with Rollback on Constraint Violation
Problem Description

You are given:

An integer array arr of length n

An integer max_value

A list of operations ops, where each operation is of the form [index, value]

Each operation represents the following action:

Increase the element at position index in the array by value.

Operations must be applied sequentially in the given order.

Constraint Rule (Rollback Condition)

If at any point during the execution of operations any element in the array becomes greater than max_value, then:

The entire array must be reset to its original state (before any operations were applied)

Execution continues with the next operation after the violating one

Previous updates are discarded


``` python
arr = [1, 2, 1]
max_value = 6
ops = [[0, 4], [1, 4], [1, 4], [2, 4]]

Operation 1: arr[0] += 4 → [5, 2, 1]
Operation 2: arr[1] += 4 → [5, 6, 1]
Operation 3: arr[1] += 4 → [5, 10, 1]  → exceeds max_value → rollback
Operation 4: arr[2] += 4 → [1, 2, 5]

[1, 2, 5]

code :
arr = [1,2,1]
op = [[0,4],[1,4],[1,4],[2,4]]
req = arr.copy()
n = len(arr)

ver = -1
maxV = 6

allver = [-1]*n

for i in range(len(op)):
    val = op[i][1]
    idx = op[i][0]
    
    if allver[idx] < ver:
        arr[idx] = req[idx]
        allver[idx] = ver
    
    arr[idx] += val
    if arr[idx] > maxV:
        ver = i
        arr[idx] = req[idx]
        allver[idx] = ver

for i in range(len(arr)):
    if allver[i] < ver:
        arr[i] = req[i]
```


Objective

Return the final state of the array after all operations have been processed according to the rules above.

def maxProduct(nums):
    n = 1
    tempList = []

    for i in nums[:-1]:
        tempList.append([i*j for j in nums[n:]])
        n = n + 1
        result = [x for y in tempList for x in y]
    
    maximum = max(result)
    print(maximum)

    
maxProduct([5, 20, 2, 6])
maxProduct([10, -20, 0, 3]) 
maxProduct([10, -20, 0, -3])
maxProduct([-1, 2])
maxProduct([-1, 0, 2])
maxProduct([5,-1, -2, 0])
maxProduct([-5, -2])
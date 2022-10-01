def twoSum(nums, target):
    for i in range(len(nums)):
        leftSide = nums[i+1:]
        
        for x in range(len(leftSide)):
            if (nums[i] + leftSide[x]) == target:
                return [i, x+i+1]

result = twoSum([2, 11, 7, 15], 9)
print(result)
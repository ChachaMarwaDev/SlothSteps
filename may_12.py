# Problem sqrt(x)
# Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

# You must not use any built-in exponent function or operator.

# For example, do not use pow(x, 0.5) in c++ or (x ** 0.5) in python.

class Solution(object):
    def mySqrt(self, x):
        if x < 2:
            return x
        
        low = 1
        high = (x // 2) + 1
        result = 0

        while low <= high:
            mid = (low + high) // 2
            if mid * mid <= x:
                result = mid
                low = mid + 1
            else:
                high = mid - 1

        return result
    
ans = Solution()
res = ans.mySqrt(2)
print(res)
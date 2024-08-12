# niu
"""
time complexity: O(n+m*SIGMA)
where SIGMA is the count of alphabet chars
"""

"""
using dp approach to save state in our patter
dpi,j -> lps where the curr char is j and we are in ith index
lps: longest prefix suffix
"""
def build_dp(sub, m):
    dp = [[0 for _ in range(26)] for _ in range(m)]

    lps = 0
    for i, char in enumerate(sub):
        for j in range(26):
            if j == ord(char)-97:
                dp[i][j] = i+1
            else:
                dp[i][j] = dp[lps][j]
                lps = dp[lps][j]

    return dp


    

s, sub = input().lower(), input().lower()
n, m = len(s), len(sub)


dp = build_dp(sub, m)

i, j, count = 0, 0, 0

while i < n:
    if s[i] == sub[j]:
        i += 1
        j += 1
    if j == m:
        count += 1
        j = dp[j-2][ord(s[i-1])-97]
    else:
        if j != 0:
            j = dp[j-1][ord(s[i-1])-97]
        else:
            i += 1


print(count)
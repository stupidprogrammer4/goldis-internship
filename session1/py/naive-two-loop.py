# niu
"""
time complexity: O(nm)
"""
s, sub = input(), input()
n, m = len(s), len(sub)
count = 0

for i in range(n-m+1):
    for j in range(m):
        if s[i+j] != sub[j]:
            break
    else:
        count += 1

print(count)

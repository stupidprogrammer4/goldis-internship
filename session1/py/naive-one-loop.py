# niu
"""
time complexity: O(nm)
"""
s, sub = input(), input()

n, m = len(s), len(sub)

i = j = count = 0

while i < n:
    if j == m:
        count += 1
        i = i - m + 1
        j = 0

    if s[i] == sub[j]:
        j += 1
    else:
        i -= j
        j = 0
    i += 1

if j == m:
    count += 1


print(count)

// niu
#include <stdio.h>
#include <stdlib.h>

// time complexity: O(nm)

int main() {
    int n, m;
    scanf("%d %d", &n, &m);
    char *str = malloc(n+1);
    char *sub = malloc(m+1);

    scanf("%s", str);
    scanf("%s", sub);

    int i=0, j=0, count=0;

    while (str[i] != '\0') {
        if (j == m) {
            count++;
            i = i - m + 1;
            j = 0;
        }

        if (str[i] == sub[j])
            j++;
        else
            i -= j, j=0;

        i++;
    }

    if (j == m)
        count++;

    free(str);
    free(sub);

    printf("%d\n", count);
}
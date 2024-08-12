// niu
#include <stdio.h>
#include <stdlib.h>

// time complexity: O(nm)

int main() {
    int n, m, i, j, count=0;
    scanf("%d %d", &n, &m);
    char *str = malloc(n+1);
    char *sub = malloc(m+1);

    scanf("%s", str);
    scanf("%s", sub);

    for (i=0; i<=n-m; i++) {
        for (j=0; j<m; j++)
            if (str[i+j] != sub[j])
                break;

        if (j == m) count++;
    }

    free(str);
    free(sub);

    printf("%d\n", count);
}
// niu
#include <stdio.h>
#include <stdlib.h>

int *dp[26];

/*
time complexity: O(n+m*SIGMA)
where SIGMA is the count of alphabet chars
*/

/*
time complexity: O(n+m*SIGMA)
where SIGMA is the count of alphabet chars

using dp approach to save state in our patter
dpi,j -> lps where the curr char is j and we are in ith index
lps: longest prefix suffix
*/

// preprocess dp array
inline void build_dfa(int m, char *sub) {
    // dynamicaly allocate memory
    for (int i=0; i<26; i++)
        dp[i] = malloc(m);

    int lps=0;
    for (int i=0; sub[i] != '\0'; i++)
        for (int j=0; j<26; j++)
            if (j == sub[i]-97)
                dp[j][i] = i+1;
            else
                dp[j][i] = dp[j][lps], lps = dp[j][lps];
}

// we must free memory that dynamical allocated
void destroy_dfa() {
    // free memory
    for (int i=0; i<26; i++) 
        free(dp[i]);
}

int main() {
    int n, m, i=0, j=0, count=0;
    scanf("%d %d", &n, &m);
    char *str = malloc(n+1);
    char *sub = malloc(m+1);

    scanf("%s", str);
    scanf("%s", sub);

    build_dfa(m, sub);
    while (str[i] != '\0') {
        if (str[i] == sub[j])
            j++, i++;

        if (j == m) {
            j = dp[str[i-1]-97][j-2];
            count++;
        }
        else {
            if (j)
                j = dp[str[i-1]-97][j-1];
            else
                i++;
        }
    }
    destroy_dfa();
    printf("%d\n", count);
}
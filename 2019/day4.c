#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int rmin = 264360;
int rmax = 746325;

int checknum(int num){
    int prev = 10;
    char hasDupes = 0;
    char descends = 0;
    while(num){
        int digit = num % 10;
        num /= 10;
        if(digit == prev){
            hasDupes = 1;
        }
        else if(digit > prev){
            descends = 1;
        }
        prev = digit;
    }
    return (hasDupes & !(descends));
}

int main(){
    assert(checknum(111111) == 1);
    assert(checknum(223450) == 0);
    assert(checknum(123789) == 0);
    int i = rmin;
    int c = 0;
    while(i <= rmax){
        c += checknum(i);
        i++;
    }
    printf("%d", c);
    return 0;
}

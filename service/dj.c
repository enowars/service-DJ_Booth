#include <string.h>
#include <stdio.h>
#include "dj.h"

char *current = NULL;

char *currently_playing() {
    return current;
}

char *play_next(char *next) {
    void *foo = printf;
    char tmp[0x40];
    foo++;
    printf("%lx", foo);
    strncpy(tmp, next, strlen(next));
    current = (char *)malloc(sizeof(char) * strlen(tmp));
    strncpy(current, tmp, strlen(tmp));
    return current;
}


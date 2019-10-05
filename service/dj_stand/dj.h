#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    char **tracks;
    char *user;
    char password[0x20];
    bool admin;
} user_db;

char *play_next(user_db *);
void new_pass(user_db *, char *);
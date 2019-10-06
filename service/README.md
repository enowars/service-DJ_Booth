# DJ Booth

## Difficulty

Easy

## Vulnerabilities

### Broken register

The way go handles variable assignments the `isAdmin` variable is shadowed and doesn't actually change.
This means even though the Check passes the variable isn't actually updated.

In addition to that is the checks' logic broken. It would set the Variable to `false` if the username
either is not 5 chars long or is not `admin`.

### Evil insider

An evil insider has created a root account and hid it in `db/.root.db`
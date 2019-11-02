# DJ Booth

## Difficulty

Easy

## Vulnerabilities

### Broken register

The way go handles variable assignments the `isAdmin` variable is shadowed and doesn't actually change.
This means even though the Check passes the variable isn't actually updated.

In addition to that is the checks' logic broken. It would set the Variable to `false` if the username
either is not 5 chars long or is not `admin`.

### Debug is enabled

The debug mode is always enabled even though the menu doesn't show it. Thus even a non admin user can
call the debug function

### Evil insider

An evil insider has created a root account and hid it in `db/.root.db`

### RCE

Due to the missing stack canaries and broken handeling of the `currently playing song`, RCE is possible
when the song name is longer 0x40 characters. The return pointer can be overwritten.

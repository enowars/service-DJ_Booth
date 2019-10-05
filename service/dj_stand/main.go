package main

// #cgo LDFLAGS: -L./ -ldj
// #include <dj.h>
import "C"

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net"
	"os"
	"strconv"
	"strings"
	"unsafe"
)

type db struct {
	Tracks   []string `json:"tracks"`
	User     string   `json:"user"`
	Password string   `json:"password"`
	Admin    bool     `json:"admin"`
}

func main() {
	ln, _ := net.Listen("tcp", ":7556")
	for {
		conn, _ := ln.Accept()
		go handle(conn)
	}
}

func handle(conn net.Conn) {
	defer conn.Close()

	conn.Write([]byte("Welcome to your personal DJ assistant.\nDo you want to [r]egister or [l]ogin?: "))
	choice, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return
	}

	choice = strings.Trim(choice, "\n")

	switch choice {
	case "r":
		register(conn)
	case "l":
		if user, ret := login(conn); ret == 0 {
			quit := false
			for !quit {
				menu(conn, user.Admin)
				conn.Write([]byte("What do you want to do? "))
				choice, err := bufio.NewReader(conn).ReadString('\n')

				if err != nil {
					conn.Write([]byte("Sorry something went wrong!"))
					return
				}

				choice = strings.ToLower(strings.Trim(choice, "\n"))

				switch choice {
				case "a":
					if add(conn, user) == -1 {
						return
					}
				case "r":
					if remove(conn, user) == -1 {
						return
					}
				case "d":
					if debug(conn) == -1 {
						return
					}
				case "l":
					list(conn, user)
				case "s":
					if selectNext(conn, user) == -1 {
						return
					}
				case "p":
					playNext(conn, user)
				case "c":
					if changePassword(conn, user) == -1 {
						return
					}
				case "q":
					return
				default:
					conn.Write([]byte(choice + " is invalid!\n"))
					continue
				}
			}
		}
	default:
		conn.Write([]byte("Sorry but I don't know what you mean with " + choice + "\n"))
	}
}

func changePassword(conn net.Conn, user db) int {
	conn.Write([]byte("New Password: "))
	newPass, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return -1
	}

	newPass = strings.Trim(newPass, "\n")
	newPassC := C.CString(newPass)
	defer C.free(unsafe.Pointer(newPassC))
	C.new_pass((*C.user_db)(unsafe.Pointer(&user)), newPassC)
	tmp, err := json.Marshal(user)

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return -1
	}

	ioutil.WriteFile("db/"+user.User+".db", tmp, 0644)
	return 0
}

func playNext(conn net.Conn, user db) {
	current := C.play_next((*C.user_db)(unsafe.Pointer(&user)))
	conn.Write([]byte("Currently Playing: " + C.GoString(current) + "\n"))
}

func selectNext(conn net.Conn, user db) int {
	conn.Write([]byte("Which song do you want to play next?"))
	for i, s := range user.Tracks {
		conn.Write([]byte(strconv.Itoa(i) + ") " + s))
	}

	conn.Write([]byte("> "))
	choice, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return -1
	}

	choice = strings.ToLower(strings.Trim(choice, "\n"))

	if c, err := strconv.Atoi(choice); err != nil || c < 0 || c >= len(user.Tracks) {
		conn.Write([]byte(choice + " is not valid!"))
		return 0
	} else {
		tmp := []string{user.Tracks[c]}
		tmp = append(tmp, user.Tracks[:c]...)
		user.Tracks = append(tmp, user.Tracks[c+1:]...)
	}
	return 0
}

func list(conn net.Conn, user db) {
	for i, t := range user.Tracks {
		conn.Write([]byte(strconv.Itoa(i) + ") " + t + "\n"))
	}
}

func debug(conn net.Conn) int {
	files, err := ioutil.ReadDir("./db/")
	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return -1
	}
	for _, f := range files {
		content, err := ioutil.ReadFile("./db/" + f.Name())
		if err != nil {
			conn.Write([]byte("Sorry something went wrong!"))
			return -1
		}
		var tmpDB db
		err = json.Unmarshal(content, &tmpDB)
		if err != nil {
			conn.Write([]byte("Sorry something went wrong!"))
			return -1
		}
		for _, t := range tmpDB.Tracks {
			conn.Write([]byte(f.Name() + ") " + t + "\n"))
		}
	}
	return 0
}

func add(conn net.Conn, user db) int {
	conn.Write([]byte("What is the name of the song?\n> "))
	songName, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return -1
	}

	songName = strings.Trim(songName, "\n")
	user.Tracks = append(user.Tracks, songName)
	return 0
}

func remove(conn net.Conn, user db) int {
	conn.Write([]byte("Which song do you want to remove?"))
	for i, s := range user.Tracks {
		conn.Write([]byte(strconv.Itoa(i) + ") " + s))
	}

	conn.Write([]byte("> "))
	choice, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return -1
	}

	choice = strings.ToLower(strings.Trim(choice, "\n"))

	if c, err := strconv.Atoi(choice); err != nil || c < 0 || c >= len(user.Tracks) {
		conn.Write([]byte(choice + " is not valid!\n"))
		return 0
	} else {
		user.Tracks = append(user.Tracks[:c], user.Tracks[c+1:]...)
	}
	return 0
}

func menu(conn net.Conn, isAdmin bool) {
	conn.Write([]byte("===============================\n"))
	conn.Write([]byte("=   Your personal DJ booth!   =\n"))
	conn.Write([]byte("===============================\n"))
	conn.Write([]byte("(A)dd a song to your list\n"))
	conn.Write([]byte("(R)emove a song from your list\n"))
	if isAdmin {
		conn.Write([]byte("(D)isplay all tracks (Debug)\n"))
	}
	conn.Write([]byte("(L)ist all songs in your list\n"))
	conn.Write([]byte("(S)elect a song to play next\n"))
	conn.Write([]byte("(P)lay the next song\n"))
	conn.Write([]byte("(C)hange your password\n"))
	conn.Write([]byte("(Q)uit\n"))
}

func register(conn net.Conn) {
	conn.Write([]byte("So you want to become a better DJ?\nWell then I need your username: "))
	username, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return
	}

	username = strings.Trim(username, "\n")

	conn.Write([]byte("And your password: "))
	password, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return
	}

	isAdmin := true
	if len(username) != 5 || username != "admin" {
		isAdmin := false
		fmt.Println("Debug: Adding user", username, "with Password:", password, ". isAdmin:", isAdmin)
	}

	password = strings.Trim(password, "\n")
	newDB := db{User: username, Password: password, Admin: isAdmin, Tracks: []string{}}
	tmp, err := json.Marshal(newDB)

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return
	}

	ioutil.WriteFile("db/"+username+".db", tmp, 0644)
}

func login(conn net.Conn) (db, int) {
	conn.Write([]byte("Welcome back!\nI need your username: "))
	username, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return db{}, -1
	}

	username = strings.Trim(username, "\n")

	conn.Write([]byte("And your password: "))
	password, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return db{}, -1
	}
	password = strings.Trim(password, "\n")

	if _, err := os.Stat("./db/" + username + ".db"); os.IsNotExist(err) {
		conn.Write([]byte("Sorry Username or Password are wrong"))
		return db{}, -1
	}

	content, err := ioutil.ReadFile("db/" + username + ".db")
	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return db{}, -1
	}

	var userDB db
	err = json.Unmarshal(content, &userDB)
	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return db{}, -1
	}

	if password != userDB.Password {
		fmt.Printf("Want=%v(%T) Have=%v(%T)", userDB.Password, userDB.Password, password, password)
		conn.Write([]byte("Sorry Username or Password are wrong!"))
		return db{}, -1
	}

	return userDB, 0
}

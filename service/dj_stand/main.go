package main

import (
	"bufio"
	"encoding/json"
	"io/ioutil"
	"net"
	"strings"
)

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
		login(conn)
	default:
		conn.Write([]byte("Sorry but I don't know what you mean with " + choice + "\n"))
	}
}

func register(conn net.Conn) {
	conn.Write([]byte("So you want to become a better DJ?\nWell then I need your username: "))
	username, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return
	}

	username = strings.Trim(username, "\n")

	conn.Write([]byte("And I need your password: "))
	password, err := bufio.NewReader(conn).ReadString('\n')

	if err != nil {
		conn.Write([]byte("Sorry something went wrong!"))
		return
	}

	isAdmin := true
	if len(username) != 5 && username != "admin" {
		isAdmin := false
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

func login(conn net.Conn) {

}

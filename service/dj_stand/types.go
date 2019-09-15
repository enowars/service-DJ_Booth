package main

import "sync"

type db struct {
	User     string   `json:"user"`
	Password string   `json:"password"`
	Tracks   []string `json:"tracks"`
	Admin    bool     `json:"admin"`
}

var (
	fileLock = new(sync.Mutex)
)

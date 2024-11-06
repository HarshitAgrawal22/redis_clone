package main

import (
	"fmt"
	"net"
)

type Peer struct {
	conn net.Conn
}

func newPeer(conn net.Conn) *Peer {
	return &Peer{
		conn: conn,
	}
}

func (p *Peer) readLoop() error {
	buf := make([]byte, 1024)
	for {
		n, err := p.conn.Read(buf)
		if err != nil {

			return err
		}
		fmt.Println(string(buf[:n]))
	}
}

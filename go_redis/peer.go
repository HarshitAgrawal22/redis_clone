package main

import "net"

type Peer struct {
	conn net.Conn
}

func newPeer(conn net.Conn) *Peer {
	return &Peer{
		conn: conn,
	}
}

func (p *Peer) readLoop() {
	server := NewServer(Config{ListenAddress: ":5001"})
	server.Start()
}

package main

import (
	// "bytes"
	"fmt"
	// "io"
	// "log"
	"net"
	// "github.com/tidwall/resp"
)

type Peer struct {
	conn  net.Conn
	msgch chan Message
}

func newPeer(conn net.Conn, msg_ch chan Message) *Peer {
	// server's msgchain is set as peer's message chain
	return &Peer{
		conn:  conn,
		msgch: msg_ch,
	}
}
func (p *Peer) Send(msg []byte) (int, error) {
	return p.conn.Write(msg)
}
func (p *Peer) readLoop() error {
	// function continously reads data from, the connection in a never ending loop
	buf := make([]byte, 1024)
	// creates a byte slice of 1024 bytes as a buffer for incoming data
	for {
		n, err := p.conn.Read(buf) // reads data into the buffer from the connection
		if err != nil {
			// if error occurs then that is returned
			return err

		}

		fmt.Println(string(buf[:n]))
		fmt.Println(len(buf[:n]))

		msgBuf := make([]byte, n) // creating a msg buffer of exact read data size
		copy(msgBuf, buf[:n])     // copying data of buffer to msgbuffer
		p.msgch <- Message{
			data: msgBuf,
			peer: p,
		} // appending msg to  peer's buffer
	}
}

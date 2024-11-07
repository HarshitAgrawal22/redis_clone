package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net"

	"github.com/tidwall/resp"
)

type Peer struct {
	conn  net.Conn
	msgch chan []byte
}

func newPeer(conn net.Conn, msg_ch chan []byte) *Peer {
	// server's msgchain is set as peer's message chain
	return &Peer{
		conn:  conn,
		msgch: msg_ch,
	}
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
		p.msgch <- msgBuf         // appendingmsg to  peer's buffer
	}
}

func (p *Peer) TestProtocol() error {
	raw := "*3\r\n$3\r\nSET\r\n$5\r\nmyKey\r\n$3\r\nbar\r\n"
	rd := resp.NewReader(bytes.NewBufferString(raw))
	for {
		v, _, err := rd.ReadValue()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("Read %s \n", v.Type())
		if v.Type() == resp.Array {
			for i, v := range v.Array() {
				fmt.Printf(" #%d %s, value: '%s'\n", i, v.Type(), v)
			}
		}
	}
	return nil
}

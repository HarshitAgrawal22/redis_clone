package main

import (
	// "io"
	// "log"
	"fmt"
	"io"
	"log"
	"net"

	"github.com/tidwall/resp"
	// "github.com/tidwall/resp"
)

type Peer struct {
	conn  net.Conn
	msgch chan Message
	delch chan *Peer
}

func newPeer(conn net.Conn, msg_ch chan Message, delCh chan *Peer) *Peer {
	// server's msgchain is set as peer's message chain
	return &Peer{
		conn:  conn,
		msgch: msg_ch,
		delch: delCh,
	}

}
func (p *Peer) Send(msg []byte) (int, error) {
	return p.conn.Write(msg)
}
func (p *Peer) readLoop() error {

	rd := resp.NewReader((p.conn))

	for {
		v, _, err := rd.ReadValue()
		if err == io.EOF {
			p.delch <- p
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		var cmd Command
		// fmt.Printf("Read %s \n", v.Type())
		if v.Type() == resp.Array {
			rawCMD := v.Array()[0]

			switch rawCMD.String() {
			case CommandClient:
				cmd = ClientCommand{
					value: v.Array()[1].String(),
				}
			case CommandGET:
				// fmt.Printf("%+v\n", v.Array())
				if len(v.Array()) != 2 {
					return fmt.Errorf("invalid number of variables for GET command")

				}

				cmd = GetCommand{
					key: v.Array()[1].Bytes(),
				}
				// return cmd
				fmt.Printf("got GET cmd %+v\n", cmd)

			case CommandSET:
				fmt.Printf("%+v\n", v.Array())
				if len(v.Array()) != 3 {
					return fmt.Errorf("invalid number of variables for SET command")

				}
				cmd = SetCommand{
					key:   v.Array()[1].Bytes(),
					value: v.Array()[2].Bytes(),
				}

				fmt.Printf("got SET cmd %+v", cmd)
			case CommandHELLO:
				cmd = HelloCommand{
					value: v.Array()[1].String(),
				}
				fmt.Printf("got HELLO cmd %+v\n", cmd)
			default:
				fmt.Println(v.Array())
				fmt.Println("unknown Command bro")
			}
			p.msgch <- Message{
				cmd:  cmd,
				peer: p,
			}
		}

	}
	return nil
}

// function continously reads data from, the connection in a never ending loop
// buf := make([]byte, 1024)
// // creates a byte slice of 1024 bytes as a buffer for incoming data
// for {
// 	n, err := p.conn.Read(buf) // reads data into the buffer from the connection
// 	if err != nil {
// 		// if error occurs then that is returned
// 		return err

// 	}

// 	fmt.Println(string(buf[:n]))
// 	fmt.Println(len(buf[:n]))

// 	msgBuf := make([]byte, n) // creating a msg buffer of exact read data size
// 	copy(msgBuf, buf[:n])     // copying data of buffer to msgbuffer
// 	p.msgch <- Message{
// 		data: msgBuf,
// 		peer: p,
// 	} // appending msg to  peer's buffer
// }

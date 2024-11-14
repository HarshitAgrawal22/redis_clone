package main

import (
	"fmt"

	"log"
	"log/slog"
	"net"

	"github.com/tidwall/resp"
)

const defaultAddress = ":5001"

type Config struct {
	// It holds the data, specifically "ListenAddress," which specifies where the server will listen for connections
	ListenAddress string
}

type Message struct {
	cmd  Command
	peer *Peer
}
type Server struct {
	// Server holds the server's settings, a list of peers, a listener, and a channel to channel new peers.
	Config                   // Embeds the config for easy access to its fields
	peers     map[*Peer]bool // map to track connected peers with *Peer as keys and boolean as value
	ln        net.Listener   // a network listener for accepting connections
	addPeerCh chan *Peer     // a channel to add peers to the server
	delPeerCh chan *Peer
	quitCh    chan struct{} // A channel for signaling server shutdown, used to gracefully stop loops.
	msgch     chan Message  // A channel for broadcasting messages to connected peers.
	kv        *KV
}

func NewServer(cfg Config) *Server {
	// we are taking cfg of type config and returning a pointer to a server
	if len(cfg.ListenAddress) == 0 {
		cfg.ListenAddress = defaultAddress
	}

	return &Server{
		Config:    cfg,
		peers:     make(map[*Peer]bool), // A map to track active peers
		addPeerCh: make(chan *Peer),     // A channel to add new peers to the server
		delPeerCh: make(chan *Peer),
		quitCh:    make(chan struct{}),
		msgch:     make(chan Message),
		kv:        NewKeyVal(),
	}
}

// will be used to start the server
func (s *Server) Start() error {
	// if the server starts successfully then the listener will be assigned to ln; if there is an error, then listener will be assigned to err
	ln, err := net.Listen("tcp", s.ListenAddress)
	if err != nil {
		return err
	}

	// the current server's listener will be assigned to server's listener
	s.ln = ln
	fmt.Printf("Server started, listening on %s\n", s.ListenAddress)

	go s.loop()
	slog.Info("server running", "ListenAdress", s.ListenAddress)
	// calling the acceptLoop to handle incoming connections
	return s.acceptLoop()
}

func (s *Server) set(key string, val string) error {
	return nil
}
func (s *Server) handleMessage(msg Message) error {
	// fmt.Println(string(msg.data))
	// cmd, err := parseCommand(string(msg.data))
	// if err != nil {
	// 	return err
	// }
	// fmt.Println(cmd, "is the cmd")
	switch v := msg.cmd.(type) {
	case ClientCommand:
		if err := resp.NewWriter(msg.peer.conn).WriteString("OK"); err != nil {
			return err
		}
	case SetCommand:
		slog.Info("Somebody wants to det a key into hashtable", "key", v.key, "val", v.value)
		err := s.kv.Set(v.key, v.value)
		if err != nil {
			return err

		}

		if err := resp.NewWriter(msg.peer.conn).WriteString("OK"); err != nil {
			return err
		}

	case GetCommand:

		val, ok := s.kv.Get(v.key)
		if !ok {
			return fmt.Errorf("key not found")

		}
		fmt.Println(val, "found the item ")
		// _, err := msg.peer.Send(val)

		if err := resp.NewWriter(msg.peer.conn).WriteString(string(val)); err != nil {

			return err
		}
	case HelloCommand:
		spec := map[string]string{
			"server": "redis",
		}
		_, err := msg.peer.Send(respWriteMap(spec))
		if err != nil {
			return fmt.Errorf("peer send error %s", err)
		}
	}
	return nil
}

func (s *Server) loop() {
	// this function waits for a peer to be received on the addPeerCh channel and adds it to peers map. if no new peer is received, it defaults to printing
	for {

		select {
		case Msg := <-s.msgch:

			// it listens for msgchannel , when it a new message is received , it prints the message
			// fmt.Println(rawMsg)

			if err := s.handleMessage(Msg); err != nil {
				slog.Error("Raw Message Error from", "err", err)
			}
			// fmt.Println(rawMsg)

		case <-s.quitCh:
			fmt.Println("quitting server")
			return

		case peer := <-s.addPeerCh:
			s.peers[peer] = true
			slog.Info("New peer connected: ", "remoteAddr", peer.conn.RemoteAddr())

		case peer := <-s.delPeerCh:
			slog.Info("Peer Disconnected ", "remoteAddr", peer.conn.RemoteAddr())
			delete(s.peers, peer)
		}
	}
}

func (s *Server) acceptLoop() error {
	// accepts incoming connections in an infinite loop. if there's an error, it logs it and continues to the next iteration. Each connection is handled concurrently by calling handleConn(conn) in a goroutine
	for {
		conn, err := s.ln.Accept()
		if err != nil {
			slog.Error("accept error", "err", err)
			continue
		}
		fmt.Printf("Accepted new connection from %s\n", conn.RemoteAddr())
		go s.handleConn(conn)
	}
}

func (s *Server) handleConn(conn net.Conn) {
	// this function is meant to handle each new connection by creating a Peer instance for the connection (newPeer(conn)).

	this_peer := newPeer(conn, s.msgch, s.delPeerCh) // here we are sending server's msg chan to new peer to access messages directly from the server of all the peers

	s.addPeerCh <- this_peer // Send the newly created Peer to the addPeerCh channel for the server to add it to its peers list

	slog.Info("new peer connected", "remoteAddress", conn.RemoteAddr())
	if err := this_peer.readLoop(); err != nil {
		// if there is a error then we log the error in the console
		slog.Error("peer read error", "err", err, "remoteAddr", conn.RemoteAddr())
	}
}

func main() {
	server := NewServer(Config{})
	log.Fatal(server.Start())
	// go func() {

	// 	log.Fatal(server.Start())
	// }()

	// time.Sleep(time.Second)
	// for i := 0; i < 10; i++ {
	// 	c, err := client.NewClient("localhost:5001")
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}
	// 	if err := c.Set(context.TODO(), fmt.Sprintf("key_%d", i), fmt.Sprintf("data_%d", i)); err != nil {
	// 		log.Fatal(err)
	// 	}
	// 	fmt.Println("SET =>", fmt.Sprintf("key_%d with data+%d", i, i))

	// 	val, err := c.Get(context.TODO(), fmt.Sprintf("key_%d", i))
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}
	// 	fmt.Printf("GET => %+v\n", string(val))
	// }

	// time.Sleep(time.Second)
	// fmt.Println(server.kv.data)
}

package main

import (
	"fmt"
	"log"
	"log/slog"
	"net"
)

const defaultAddress = ":5001"

type Config struct {
	// It holds the data, specifically "ListenAddress," which specifies where the server will listen for connections
	ListenAddress string
}

type Server struct {
	// Server holds the server's settings, a list of peers, a listener, and a channel to channel new peers.
	Config                   // Embeds the config for easy access to its fields
	peers     map[*Peer]bool // map to track connected peers with *Peer as keys and boolean as value
	ln        net.Listener   // a network listener for accepting connections
	addPeerCh chan *Peer     // a channel to add peers to the server
	quitCh    chan struct{}  // A channel for signaling server shutdown, used to gracefully stop loops.
	msgch     chan []byte    // A channel for broadcasting messages to connected peers.
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
		quitCh:    make(chan struct{}),
		msgch:     make(chan []byte),
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

func (s *Server) handleRawMessage(rawMsg []byte) error {
	fmt.Println(string(rawMsg))
	return nil
}

func (s *Server) loop() {
	// this function waits for a peer to be received on the addPeerCh channel and adds it to peers map. if no new peer is received, it defaults to printing
	for {

		select {
		case rawMsg := <-s.msgch:

			// it listens for msgchannel , when it a new message is received , it prints the message
			if err := s.handleRawMessage(rawMsg); err != nil {
				slog.Error("Raw Message Error from", "err", err)
			}
			fmt.Println(rawMsg)

		case <-s.quitCh:
			fmt.Println("qutting server")
			return
		case peer := <-s.addPeerCh:
			s.peers[peer] = true
			fmt.Printf("New peer connected: %v\n", peer.conn.RemoteAddr())

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

	this_peer := newPeer(conn, s.msgch) // here we are sending server's msg chan to new peer to access messages directly from the server of all the peers
	this_peer.TestProtocol()
	s.addPeerCh <- this_peer // Send the newly created Peer to the addPeerCh channel for the server to add it to its peers list

	slog.Info("new peer connected", "remoteAddress", conn.RemoteAddr())
	if err := this_peer.readLoop(); err != nil {
		// if there is a error then we log the error in the console
		slog.Error("peer read error", "err", err, "remoteAddr", conn.RemoteAddr())
	}
}

func main() {

	server := NewServer(Config{})
	if err := server.Start(); err != nil {
		log.Fatal(err)
	}

}

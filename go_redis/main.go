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
	quitCh    chan struct{}
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

func (s *Server) loop() {
	// this function waits for a peer to be received on the addPeerCh channel and adds it to peers map. if no new peer is received, it defaults to printing
	for {

		select {
		case <-s.quitCh:
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
	peer := newPeer(conn)
	s.addPeerCh <- peer

	slog.Info("new peer connected", "remoteAddress", conn.RemoteAddr())
	go peer.readLoop()
}

func main() {
	server := NewServer(Config{})
	if err := server.Start(); err != nil {
		log.Fatal(err)
	}
}

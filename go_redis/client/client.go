package client

import (
	"bytes"
	"context"
	"net"

	"github.com/tidwall/resp"
)

type Client struct {
	addr string
	conn net.Conn
}

func NewClient(addr string) (*Client, error) {
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		return nil, err
	}
	return &Client{
		addr: addr,
		conn: conn,
	}, nil
}

// while working with  tcp connection we need to have context
func (c *Client) Set(ctx context.Context, key string, value string) error {

	var buf bytes.Buffer
	wr := resp.NewWriter(&buf)

	wr.WriteArray([]resp.Value{
		resp.StringValue("set"),
		resp.StringValue(key),
		resp.StringValue(value),
	})
	// _, err = conn.Write(buf.Bytes())
	_, err := c.conn.Write(buf.Bytes())

	return err
}

func (c *Client) Get(ctx context.Context, key string) (string, error) {

	var buf bytes.Buffer
	wr := resp.NewWriter(&buf)

	wr.WriteArray([]resp.Value{
		resp.StringValue("get"),
		resp.StringValue(key),
	})
	// _, err = conn.Write(buf.Bytes())
	_, err := c.conn.Write(buf.Bytes())
	if err != nil {
		return "", err
	}

	b := make([]byte, 1024)

	n, err := c.conn.Read(b)

	return string(b[:n]), err
}

package client

import (
	"bytes"
	"context"
	"net"

	"github.com/tidwall/resp"
)

type Client struct {
	addr string
}

func NewClient(addr string) *Client {
	return &Client{
		addr: addr,
	}
}

// while working with  tcp connection we need to have context
func (c *Client) Set(ctx context.Context, key string, value string) error {
	conn, err := net.Dial("tcp", c.addr)
	if err != nil {
		return err
	}
	var buf bytes.Buffer

	wr := resp.NewWriter(&buf)

	wr.WriteArray([]resp.Value{
		resp.StringValue("SET"),
		resp.StringValue(key),
		resp.StringValue(value),
	})
	_, err = conn.Write(buf.Bytes())

	return err
}

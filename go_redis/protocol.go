package main

import (
	"bytes"
	"fmt"
	"io"
	"log"

	"github.com/tidwall/resp"
)

const (
	CommandSET    = "set"
	CommandGET    = "get"
	CommandHELLO  = "hello"
	CommandClient = "client"
)

type Command interface {
}
type SetCommand struct {
	key, value []byte
}
type GetCommand struct {
	key, value []byte
}

func parseCommand(raw string) (Command, error) {
	// raw := "*3\r\n$3\r\nSET\r\n$5\r\nmyKey\r\n$3\r\nbar\r\n"
	rd := resp.NewReader(bytes.NewBufferString(raw))
	for {
		v, _, err := rd.ReadValue()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		// fmt.Printf("Read %s \n", v.Type())
		if v.Type() == resp.Array {
			for i, value := range v.Array() {
				fmt.Printf(" #%d %s, value: '%s'\n", i, v.Type(), v)
				switch value.String() {

				case CommandGET:
					// fmt.Printf("%+v\n", v.Array())
					if len(v.Array()) != 2 {
						return nil, fmt.Errorf("invalid number of variables for GET command")

					}

					cmd := GetCommand{
						key: v.Array()[1].Bytes(),
					}
					return cmd, nil
				case CommandSET:
					fmt.Printf("%+v\n", v.Array())
					if len(v.Array()) != 3 {
						return nil, fmt.Errorf("invalid number of variables for SET command")

					}

					cmd := SetCommand{
						key:   v.Array()[1].Bytes(),
						value: v.Array()[2].Bytes(),
					}
					return cmd, nil
				}
			}
		}

		return nil, fmt.Errorf("invalid or unknown command received ; %s", raw)
	}
	return nil, fmt.Errorf("invalid or unknown command received ; %s", raw)

}

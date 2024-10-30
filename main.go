import "net"
type Config  struct{
    ListenAddress string
}

type Server struct {
    Config
    ln net.Listener
}


func main(){
    
}
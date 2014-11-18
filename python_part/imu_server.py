import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from serial import Serial
import time
import thread

client = []
angle = [0.0, 0.0, 0.0]
line = None

port = Serial(port = "/dev/ttyACM0", baudrate = 115200)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        
class IMUHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global client
        client.append(self)
        
    def on_close(self):
        global client
        client.remove(self)
        
    def on_message(self, message):
        pass
        
    def write(message):
        self.write_message(message)

def loopRead() :
    global angle
    global line

    while True :
        line = port.readline().strip()


def loopSend() :
    print line
    for i in range(0, len(client)) :
        client[i].write_message(line);

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/imu", IMUHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    main_loop = tornado.ioloop.IOLoop.instance()
    thread.start_new_thread(loopRead, ())
    scheduler = tornado.ioloop.PeriodicCallback(loopSend,20)
    scheduler.start()
    main_loop.start()


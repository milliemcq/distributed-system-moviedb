import Pyro4

@Pyro4.expose
class Hello(object):
    def say_hello(self, name):
        return "Hello, {0}: " \
               "Sucessful remote invocation!".format(name)

daemon = Pyro4.Daemon()
uri = daemon.register(Hello)

print("Server Ready: Object uri = ", uri)
daemon.requestLoop()
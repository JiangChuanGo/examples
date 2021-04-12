import atexit

def on_exit(*args):
    print("I'm quiting.", args)


atexit.register(on_exit)
atexit.register(on_exit, "I will miss you!")

# this will unregister all on exit callbacks named 'on_exit'
#atexit.unregister(on_exit)

@atexit.register
def func():
    print("I'm decorated callback.")

print("Start.")

print("End.")

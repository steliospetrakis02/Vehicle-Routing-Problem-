from threading import Timer

print('Code Execution Started')

def display():
    print('Welcome to Guru99 Tutorials')

t = Timer(5, display)  
t.start()
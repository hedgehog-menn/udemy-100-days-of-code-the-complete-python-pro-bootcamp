from flask import Flask
import random

print(random.__name__)
print(__name__)

@app.root('/')
def hello_world()
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()

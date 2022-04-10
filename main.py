import sys
sys.path.append('~/Projects/smartcar/modules/freenove')
from flask import Flask,send_from_directory

app = Flask(__name__)

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def send_root(path):
    print("Path is", path)
    return send_from_directory('ui', path)

from Motor import *            
motor=Motor()          
@app.route('/car/<action>')
def move_motor(action): 
    if action == 'forward':
        motor.setMotorModel(1000,1000,1000,1000)       #Forward
        print ("The car is moving forward")
    elif action == 'reverse':
        motor.setMotorModel(-1000,-1000,-1000,-1000)   #Back
        print ("The car is going backwards")    
    elif action == 'left':
        motor.setMotorModel(-1500,-1500,2000,2000)       #Left 
        print ("The car is turning left")  
    elif action == 'right':
        motor.setMotorModel(2000,2000,-1500,-1500)       #Right 
        print ("The car is turning right")  
    else:
        motor.setMotorModel(0,0,0,0)                   #Stop
        print ("The car is stopped")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
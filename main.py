import sys
import json
sys.path.append('/home/pi/Projects/smartcar/modules/freenove')
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
        return json.dumps({'status': 'Forward'})
    elif action == 'reverse':
        motor.setMotorModel(-1000,-1000,-1000,-1000)   #Back
        print ("The car is going backwards")    
        return json.dumps({'status': 'Reverse'})
    elif action == 'left':
        motor.setMotorModel(-1500,-1500,2000,2000)       #Left 
        print ("The car is turning left")  
        return json.dumps({'status': 'Left'})
    elif action == 'right':
        motor.setMotorModel(2000,2000,-1500,-1500)       #Right 
        print ("The car is turning right")  
        return json.dumps({'status': 'Right'})
    else:
        motor.setMotorModel(0,0,0,0)                   #Stop
        print ("The car is stopped")
        return json.dumps({'status': 'Stop'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',ssl_context='adhoc')
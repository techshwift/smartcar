import sys
import json
import time
sys.path.append('/home/pi/Projects/smartcar/modules/freenove')
sys.path.append('/home/pi/.local/lib/python2.7/site-packages')
print("Looking for modules in: ", sys.path)

from modules.freenove.Ultrasonic import Ultrasonic
from modules.freenove.servo import Servo
from modules.freenove.Buzzer import Buzzer
from modules.freenove.Motor import Motor

from flask import Flask,send_from_directory

app = Flask(__name__)

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def send_root(path):
    print("Path is", path)
    return send_from_directory('ui', path)

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

ultrasonic = Ultrasonic()
buzzer = Buzzer()
servo = Servo()
@app.route('/scan')
def scan():
    while(True):
        if ultrasonic.get_distance() < 10:
            print ("Obstruction detected. Reversing")
            move_motor('stop')
            print ("Looking around... ")
            servo.setServoPwm('0', 0)
            print("Distance to obstacle on the left: ", ultrasonic.get_distance())
            time.sleep(0.1)
            servo.setServoPwm('0', 180)
            print("Distance to obstacle on the right: ", ultrasonic.get_distance())
            time.sleep(0.1)
        else:
            move_motor('forward')


if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))
    app.run(debug=True, host='0.0.0.0')
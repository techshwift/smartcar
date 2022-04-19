import sys
import json
import time
sys.path.append('/home/pi/Projects/smartcar/modules/freenove')
sys.path.append('/home/pi/.local/lib/python2.7/site-packages')
print("Looking for modules in: ", sys.path)

# from modules.freenove.Ultrasonic import Ultrasonic
# from modules.freenove.servo import Servo
# from modules.freenove.Buzzer import Buzzer
# from modules.freenove.Motor import Motor
from Ultrasonic import Ultrasonic
from servo import Servo
from Buzzer import Buzzer
from Motor import Motor

from flask import Flask,send_from_directory

app = Flask(__name__)

@app.route('/', defaults={'path': 'index.html'})
#@app.route('/<path>')
def send_root(path):
    print("Path is", path)
    return send_from_directory('ui', path)

motor=Motor()  
motor.setMotorModel(0,0,0,0)        
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
@app.route('/scan/<action>')
def scan(action):
    motor.setMotorModel(0,0,0,0)      
    servo.setServoPwm('0', 90)  
    while(True):
        if ultrasonic.get_distance() < 30:
            print ("Obstruction detected. Stop and look around")
            move_motor('stop')
            for i in range(90,1,-1):
                servo.setServoPwm('0',i)
                print("Distance to obstacle: ", ultrasonic.get_distance())
                time.sleep(0.01)
            for i in range(1,179,1):
                servo.setServoPwm('0',i)
                print("Distance to obstacle: ", ultrasonic.get_distance())
                time.sleep(0.01)
            for i in range(179,90,-1):
                servo.setServoPwm('0',i)
                print("Distance to obstacle: ", ultrasonic.get_distance())
                time.sleep(0.01)

            return json.dumps({'status':'Looking around'})
        else:
            move_motor('forward')

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))
    app.run(debug=True, host='0.0.0.0')
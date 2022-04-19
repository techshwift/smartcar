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
    dist_to_obst_right = 200
    dist_to_obst_left = 200
    dist_to_obst_front = 200
    while(True):
        if ultrasonic.get_distance() <= 15:
            dist_to_obst_front = 15
            print ("Obstruction detected. Stop and look around")
            move_motor('stop')
            for i in range(90,1,-1):
                servo.setServoPwm('0',i)
                if i == 1:
                    dist_to_obst_left = ultrasonic.get_distance()
                    print("Distance to obstacle on left: ", dist_to_obst_left)
                time.sleep(0.01)
            for i in range(1,179,1):
                servo.setServoPwm('0',i)
                if i == 179:
                    dist_to_obst_right = ultrasonic.get_distance()
                    print("Distance to obstacle: ", dist_to_obst_right)
                time.sleep(0.01)
            for i in range(179,90,-1):
                servo.setServoPwm('0',i)
                if i == 90:
                    print("Returned to normal position")
                time.sleep(0.01)

            if dist_to_obst_left > 15 and dist_to_obst_left >= dist_to_obst_right:
                move_motor('left')
                time.sleep(0.75)
                move_motor('forward')
            elif dist_to_obst_right > 15:
                move_motor('right')
                time.sleep(0.75)
                move_motor('forward')
            else:
                move_motor('right')
                time.sleep(1.5)
                move_motor('forward')

            #return json.dumps({'status':'Looking around'})
        else:
            move_motor('forward')

if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))
    app.run(debug=True, host='0.0.0.0')
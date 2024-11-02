from inputs import get_gamepad
import math
import threading

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode
        lx = self.LeftJoystickX
        ly = self.LeftJoystickY
        lpress = self.LeftThumb
        rpress = self.RightThumb
        back = self.Back
        start = self.Start
        a = self.A
        b = self.B
        x = self.X 
        y = self.Y 
        rx = self.RightJoystickX
        ry = self.RightJoystickY
        lb = self.LeftBumper
        rb = self.RightBumper
        lt = self.LeftTrigger
        rt = self.RightTrigger
        lx = int(10*lx)
        ly = int(10*ly)
        rx = int(10*rx)
        ry = int(10*ry)
        lt = int(10*lt/4)
        rt = int(10*rt/4)


        #0-9 = ok range (10 = just value of raw 1.0 = not really important)
        lx = -9 if lx == -10 else lx
        ly = -9 if ly == -10 else ly
        rx = -9 if rx == -10 else rx
        ry = -9 if ry == -10 else ry
        lt = -9 if lt == -10 else lt
        rt = -9 if rt == -10 else rt
        lx = 9 if lx == 10 else lx
        ly = 9 if ly == 10 else ly
        rx = 9 if rx == 10 else rx
        ry = 9 if ry == 10 else ry
        lt = 9 if lt == 10 else lt
        rt = 9 if rt == 10 else rt

        #as short as possible = good
        buttonsum = 0
        
        #joystick presses
        buttonsum += 512 if lpress==1 else 0
        buttonsum += 256 if rpress==1 else 0
        
        #other
        buttonsum += 128 if back==1 else 0
        buttonsum += 64 if start==1 else 0
        
        #triggers
        buttonsum += 32 if lb==1 else 0
        buttonsum += 16 if rb==1 else 0
        
        #buttons
        buttonsum += 8 if a==1 else 0
        buttonsum += 4 if b==1 else 0
        buttonsum += 2 if x==1 else 0
        buttonsum += 1 if y==1 else 0
        
        return [lt, rt, lx, ly, rx, ry, buttonsum]



    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.Y = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state




def limit_100(val): # Limits a value to +- 100
    if val > 100:
        return 100
    elif val < -100:
        return -100
    else:
        return val

#gather angular velocity points


#pid controller
class PID_controller:
    def __init__(self, kp, ki, kd, setpoint=0, duty_cycle_min=0, duty_cycle_max=1.0):
        self.kp=kp
        self.ki=ki
        self.kd=kd

        self.setpoint=setpoint
        self.last_time = 0.0
        self.pre_error=0
        self.integral=0.0
        self.duty_cycle_min=duty_cycle_min
        self.duty_cycle_max=duty_cycle_max
    
    def update(self, current_value):
        dt=1
        error = self.setpoint - current_value
        # if current_time == 0.0:
        #     dt=1.0
        # else: 
        #     dt=current_time - self.last_time
            
        self.integral += error * dt
        derivative = (error - self.pre_error) / dt
        
        PID_value = limit_100(self.kp*error + self.ki*self.integral + self.kd*derivative)
        
        self.pre_error=error
        
        #treat PID output
        norm=(PID_value)/100
        value = norm
        
        return value
            
    def set_point(self, setpoint):
        self.setpoint=setpoint
        self.reset_intergral()
        
    def reset(self):
        self.integral = 0.0
        self.previous_error = 0.0
        self.last_time = None
        
    def reset_intergral(self):
        self.integral=0.0
                

class pid:
    def __init__(self): 
        #controller
        self.setpoint = 0.0
        
        # PID gains
        kp = 1.0
        ki = 0.1
        kd = 0.01
        
        self.pid_controller_x = PID_controller(kp, ki, kd, setpoint=self.setpoint)
        self.pid_controller_y = PID_controller(kp, ki, kd, setpoint=self.setpoint)
        
        current_time = 0.0
        print("test PID control...")
    
        debug_signals = []
    
    
    def uppdate(self, pitch, heading ):
        # hener inn verdier
        self.pitch= 0
        self.heading= 0
        
        
        self.current_value_x = self.pitch
        self.current_value_y = self.heading
        
        self.output_x = self.pid_controller_x.update(self.current_value_x)
    
        self.output_y = self.pid_controller_y.update(self.current_value_y)
    
    
        #print(output_x,output_y)

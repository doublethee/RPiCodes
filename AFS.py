import time

# Import the ADXL345 module.
import Adafruit_ADXL345

def ace ():
  # Create an ADXL345 instance.
  accel = Adafruit_ADXL345.ADXL345()

  while True:
      # Read the X, Y, Z axis acceleration values and print them.
      x, y, z = accel.read()
      print('X={0}, Y={1}, Z={2}'.format(x, y, z))
      # Wait half a second and repeat.
      time.sleep(1.5)

  #print('Printing X, Y, Z axis values, press Ctrl-C to quit...')
  return(x)



def AFS(a, pwm, dep, phi):
  import numpy as np 
  table =np.genfromtxt("SAMPLE/PWM&Thrust.txt")
  PWM = table[:, 0]
  Fthrust = table[:, 1]
  import math
  aa =math.floor((pwm - 1480) / 10) + 1
  bb =math.ceil((pwm - 1480) / 10) + 1
  Ft = Fthrust[int(aa)] + (Fthrust[int(bb)] - Fthrust[int(aa)]) * ((pwm - PWM[int(aa)]) / 10)
  Area = 0.35
  den = 998
  cd = 0.461
  m = 6.223
  Fr = m * a
  Fdsub = Ft - Fr
  if Fdsub < 0: 
    print ("Input of Pulse Width Is Small")
    vel = 0
  vel = math.sqrt(Fdsub / (0.5 * Area * den * cd))
  u = vel
  c = 0.12
  b = 0.2
  vv = 0.000001139
  Reylp = u * c / vv
  vfl = 0.000009
  if Reylp < 60000:
    textfile = "SAMPLE/Reynold50000.txt"
  textfile = "SAMPLE/Reynold100000.txt"
  data = np.genfromtxt(textfile)
  angle = data[:,0]
  cl = data[:,1]
  cd = data[:,2]
  Area = b * c
  den = 998
  jj=len(angle)
  for n in range(jj):
    ang = angle[int(n)]
    Cl = cl[int(n)]
    Fl= Area * den * u** 2 * Cl
    if dep == 1:
      depnum = 0
      opert=20
    elif dep == 6:
      depnum = 3
      opert=0
    elif dep == 2 or dep == 3:
      depnum = 1
      opert=0
    else:
      depnum = 2
      opert=20
    if opert == 0:
      time=0.0
    seg=opert//5+1
    time=[i*5 for i in range(seg)]
    dt=time
    W = .00025 * den * depnum
    diff =np.asarray(Fl)* 2 - W - vfl *np.asarray(dt)*den
    angleattack = ang
    if dep ==2:
        diff = diff
        if diff < 0:
          break 
    elif dep ==4:
        diff = diff
        if diff < 0:
          break 
    elif dep > 5:
        diff = diff
        if diff > 1:
          break
    else:
        diff = diff
        if np.all(diff>0):
          if ang == angle[1]:
            smalerror = 0
          else:
            Fln = Area * den * u ** 2 * cl[int(n-1)]
            DF = Fln - W
            smalerror = 0.25 * DF/ (DF + diff)
          angleattack = angleattack - (0.25 - smalerror)
          break
  print (angleattack)
  cy = 0.1275
  by = 0.06
  Reylpy = u * cy / vv
  phir = phi *3.141592657/180
  tim=15
  phiac = phir * 2 / (tim ** 2)
  if Reylpy < 50000:
    textfiley="SAMPLE/naca2412_50000.txt"
  textfiley="SAMPLE/naca2412_100000.txt"
  data1= np.genfromtxt(textfiley)
  angley = data1[:,0]
  cly = data1[:,1]
  cdy = data1[:,2]
  ron = 0.05
  L = 0.4938
  rin = 0.047
  mt = 6.223
  Areay = by * cy
  Izz = 0.25 * mt * (ron ** 2 + rin ** 2 + L ** 2 / 3)
  kk=len(angley)
  for ii in range(kk):
    angyaw = angley[int(ii)]
    Cly = cly[int(ii)]
    Fly = Areay * den * u ** 2 * Cly
    torq = Fly * L
    torqa = Izz * phiac
    diffy = torq - torqa
    if diffy > 0:
      phiservo = angyaw
      break
  print (phiservo)
  
main (): 
  a = ace
  b = 1711
  c = 6
  d = 10
    
    fins = AFS(a,b,c,d)
    
if__name__ == "__main__":
   main()

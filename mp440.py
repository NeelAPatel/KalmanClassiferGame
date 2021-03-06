import inspect
import sys
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as pyplot

'''
Raise a "not defined" exception as a reminder 
'''


def _raise_not_defined():
	print "Method not implemented: %s" % inspect.stack()[1][3]
	sys.exit(1)


# 5 formulas
def kf_predictStateEstimate(A, xPrev, B, U):
	predX = A * xPrev + B * U
	#predX = xPrev + U
	return predX

def kf_predictErrorCovariance(A, pPrev, Q):
	
	predP = A * pPrev * np.transpose(A) + Q
	#predP = pPrev + Q
	return predP

def kf_updateKalmanGain(P, H, R):
	return P * np.transpose(H) * np.linalg.inv(H * P * np.transpose(H) + R)
	#return P *  np.linalg.inv(P + R)

def kf_updateStateEstimate(X, kalman, H, Z):
	return X + kalman * (Z - H * X)
	#return np.linalg.inv(X) + kalman * Z - np.linalg.inv(X)

def kf_updateEstimateCovariance(H, kalman, P):
	
	return (np.identity(2) - kalman * H) * P
	#return (np.identity(2) - kalman ) * P


'''
Kalman 2D
'''
def kalman2d(data, scale=1):
	estimated = []
	
	#Noise Calculations
	Q = np.matrix([[0.0001, 0.00002], [0.00002, 0.0001]])
	R = np.matrix([[0.01, 0.005], [0.005, 0.02]])
	
	#Identity matricies
	Amx = np.identity(2)
	Bmx = np.identity(2)
	Hmx = np.identity(2)
	print("DATA VALS")
	print data
	print("ESTIMATED VALS")
	
	#initial estimation
	lambdaScaling = scale
	pPrev = lambdaScaling * np.identity(2)
	
	X = np.transpose(np.matrix([0,0]))
	
	estimated.append(X)
	
	index = 0
	for dat in data:
		uVal = np.matrix([dat[0], dat[1]])
		zVal = np.matrix([dat[2], dat[3]])
		uVal = np.transpose(uVal)
		zVal = np.transpose(zVal)
		
		xPrev = estimated[index]
		#use functions
		xPredict = kf_predictStateEstimate(Amx, xPrev, Bmx, uVal)
		pPredict = kf_predictErrorCovariance(Amx, pPrev, Q)
		kalmanGain = kf_updateKalmanGain(pPredict, Hmx, R)
		xUpdate = kf_updateStateEstimate(xPredict, kalmanGain, Hmx,zVal)
		pUpdate = kf_updateEstimateCovariance(Hmx, kalmanGain, pPredict)
		pPrev = pUpdate
		
		estimated.append(xUpdate)
		index += 1
	
	print estimated
	return estimated


'''
Plotting
'''
def plot(data, output):
	#set up plot
	dataX = []
	dataY = []
	outX = []
	outY = []
	
	# 3rd and 4th values, Z1 Z2
	for dat in data:
		dataX.append(dat[2])
		dataY.append(dat[3])
	
	for out in output:
		outX.append(out.item(0))
		outY.append(out.item(1))
	
	#Red
	lineA = pyplot.plot(outX, outY, 'ro')
	lineA = pyplot.plot(outX, outY, 'r-')
	lineA = pyplot.plot(outX, outY, label = "Estimated Position")
	
	#Blue
	lineB = pyplot.plot(dataX, dataY, 'bo')
	lineB = pyplot.plot(dataX, dataY, 'b-')
	lineB = pyplot.plot(dataX, dataY, label="Observed position")
	
	pyplot.setp(lineA, color = 'Red')
	pyplot.setp(lineB, color = 'Blue')
	pyplot.grid(color='Grey', linestyle='-', linewidth=0.5)
	pyplot.axis([2, 9, -2.5, 1.0])
	pyplot.xlabel('X')
	pyplot.ylabel('Y')
#pyplot.ion()
	pyplot.legend()
	pyplot.show()
	
	
	
	return


'''
Kalman 2D 
'''

global arrXUpdates
global arrPUpdates
global count

def _KALMANCALCULATION_(ux, uy, ox, oy,arrXUpdates, arrPUpdates,reset):

	
	Amx = np.identity(2)
	Bmx = np.identity(2)
	Hmx = np.identity(2)
	Q = np.matrix([[2, 0.5], [0.5, 2]])  # Q = np.matrix([[0.0001, 0.00002], [0.00002, 0.0001]])
	R = np.matrix([[200, 50], [50, 300]])  # R = np.matrix([[0.01, 0.005], [0.005, 0.02]])
	
	# Calculations
	uVal = [ux, uy]
	zVal = [ox, oy]
	uVal = np.transpose(uVal)
	zVal = np.transpose(zVal)
	
	# get latest value from arrays
	xPrev = arrXUpdates[len(arrXUpdates) - 1]
	pPrev = arrPUpdates[len(arrPUpdates) - 1]
	
	xPredict = kf_predictStateEstimate(Amx, xPrev, Bmx, uVal)
	pPredict = kf_predictErrorCovariance(Amx, pPrev, Q)
	kalmanGain = kf_updateKalmanGain(pPredict, Hmx, R)
	xUpdate = kf_updateStateEstimate(xPredict, kalmanGain, Hmx, zVal)
	pUpdate = kf_updateEstimateCovariance(Hmx, kalmanGain, pPredict)
	
	return (xUpdate,pUpdate)


def kalman2d_shoot(ux, uy, ox, oy, reset=False):
	decision = (0, 0, False)
	#uxuy = u value || oxoy = z value
	if reset == True:
		global arrXUpdates
		arrXUpdates = [[0, 0]]
		global arrPUpdates
		arrPUpdates = [(2 * np.identity(2))]
		global count
		count = 1
	
	
	#(xUpdate, pUpdate) = _KALMANCALCULATION_(ux,uy,ox,oy,arrXUpdates, arrPUpdates, reset)
	Amx = np.identity(2)
	Bmx = np.identity(2)
	Hmx = np.identity(2)
	Q = np.matrix([[2, 0.5], [0.5, 2]])  # Q = np.matrix([[0.0001, 0.00002], [0.00002, 0.0001]])
	R = np.matrix([[200, 50], [50, 300]])  # R = np.matrix([[0.01, 0.005], [0.005, 0.02]])
	
	# Calculations
	uVal = [ux, uy]
	zVal = [ox, oy]
	uVal = np.transpose(uVal)
	zVal = np.transpose(zVal)
	
	# get latest value from arrays
	xPrev = arrXUpdates[len(arrXUpdates) - 1]
	pPrev = arrPUpdates[len(arrPUpdates) - 1]
	
	xPredict = kf_predictStateEstimate(Amx, xPrev, Bmx, uVal)
	pPredict = kf_predictErrorCovariance(Amx, pPrev, Q)
	kalmanGain = kf_updateKalmanGain(pPredict, Hmx, R)
	xUpdate = kf_updateStateEstimate(xPredict, kalmanGain, Hmx, zVal)
	pUpdate = kf_updateEstimateCovariance(Hmx, kalmanGain, pPredict)
	# ===============
	
	# use xupdate to shoot @ coordinates
	xlow1 = xUpdate[0].item(0)
	xlow2 = xUpdate[0].item(1)
	
	#use pudpate to find good range
	plow1 = pUpdate[0].item(0)
	plow2 = pUpdate[0].item(1)
	
	#print
	#print (count)
	# print("PUpdate 0: " + str(pUpdate[0]))
	# print("XUpdate 0: " + str(xUpdate[0]))
	# print("ABS: " + str(abs(ox - xlow1)) + " " + str(abs(oy - xlow2)))
	
	
	if count >= 199:
		decision = (xlow1, xlow2, True)
		return decision

	# if (plow2 < 4.76) :
	# if (plow2 < 0.001):
	if (abs(ox - xlow1) <= 4.5):
		# print("SHOOT!")
		# print(str(xUpdate[0]) + str(xUpdate[1]))
		# print(str(pUpdate[0]) + str(pUpdate[1]))
		# print(str((ox, oy)) + str((ux,uy)))
		# print((xlow1, xlow2))
		# print((plow1, plow2))
		decision = (xlow1, xlow2, True) #shoot
	else:
		decision = (xlow1, xlow2, False)
	
	arrXUpdates.append(xUpdate)
	arrPUpdates.append(pUpdate)
	
	#print("========")
	
	count += 1
	
	return decision


'''
Kalman 2D 
'''


def kalman2d_adv_shoot(ux, uy, ox, oy, reset=False):
	decision = kalman2d_shoot(ux,uy,ox,oy,reset)
	return decision

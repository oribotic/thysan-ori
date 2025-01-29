
import math
from numpy import pi, sin
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

def sin2(a):
    return math.sin(a)*math.sin(a)

def tan2(a):
    return math.tan(a)*math.tan(a)
    
def distributeH(start, end, iterations):
    total = end - start
    iterationstep = total/iterations
    iterationsteps = int(total/iterationstep)
    hdata = []
    for i in range(iterationsteps):
        hdata.append(start + i*iterationstep)
    hdata.append(end)
    return hdata

def getMinH(a,b,c):
    return math.sqrt(abs(math.pow(a-b, 2) - math.pow(c,2)))

def getMaxH(a,b,c):
    return math.sqrt(abs(math.pow(a+b, 2) - math.pow(c,2)))
    
def getD(h,c):
    return math.sqrt(math.pow(c,2) + math.pow(h,2))

def getZeroH(a,b,c):
     return math.sqrt(abs(a**2 - (b+c)**2))

def sin2(a):
	return math.sin(a)*math.sin(a)

def tan2(a):
	return math.tan(a)*math.tan(a)
    
def getRigidKinematicAngle (sectorAngles, pDegrees):
    # p = angle in degrees
    p = math.radians(pDegrees)
    a1 = sectorAngles[0]
    a2 = sectorAngles[1]
    a3 = sectorAngles[2]
    a4 = sectorAngles[3]
    cosa2 = math.cos(a2)
    e1 = 2*math.sin(a1)*math.sin(a2)*math.tan(p/2)
    e2 = 4*sin2(a1)*sin2(a3)*tan2(p/2) - (cosa2 - math.cos(a1 - a3 - a4) + (cosa2 - math.cos(a1 + a3 - a4))* tan2(p/2))* (cosa2 - math.cos(a1 + a3 + a4) + (cosa2 - math.cos(a1 - a3 + a4))* tan2(p/2)) 
    e3 = cosa2 - math.cos(a1 - a3 - a4) + (cosa2 - math.cos(a1 + a3 - a4))* tan2(p/2)
    halftanP = e1 * math.sqrt(abs(e2))/e3
    P = 2*math.atan(halftanP)
    P_ = -2*math.atan(halftanP)
    return P, P_

def ZimmermanRigidCheck (rigid, basePolygonSides): 
    a1, a2, a3, a4 = getSectorAngles(rigid, basePolygonSides, "zimmerman")
    if abs(a1 - a4) >= abs(a2 - a3):
        return True
    else:
        return False

def getSectorAngles(sectorAdjacentToDrivingAngle, basePolygonSides, order="foschi"):
    # the edge of the polygon is truncated, doubling the number of sides
    # ie. a triangle base side, because an irregular hexagon after truncating
    sides = basePolygonSides*2 
    polygonAngle = ((sides - 2)*180)/sides
    print ("[getSectorAngles]", basePolygonSides, sectorAdjacentToDrivingAngle, polygonAngle)
    sectorAdjacentToJaw = 360 - 90 - polygonAngle - sectorAdjacentToDrivingAngle
    if order == "zimmerman":
        # sector angles are returned in the order for the zimmerman check
        sectorAnglesDegrees = [polygonAngle, 90, sectorAdjacentToJaw, sectorAdjacentToDrivingAngle]
        a1 = sectorAnglesDegrees[0]
        a2 = sectorAnglesDegrees[1]
        a3 = sectorAnglesDegrees[2]
        a4 = sectorAnglesDegrees[3]
    if order == "foschi":
        # sector angles are returned in the order for rigid kinematics equations by Foschi et al 
        sectorAnglesDegrees = [90, sectorAdjacentToJaw, sectorAdjacentToDrivingAngle, polygonAngle]
        a1 = sectorAnglesDegrees[0]
        a2 = sectorAnglesDegrees[1]
        a3 = sectorAnglesDegrees[2]
        a4 = sectorAnglesDegrees[3]
    print (order, a1, a2, a3, a4)
    return a1, a2, a3, a4

def getGraphData(a,b,c,rigid,iterations):
    sectorAnglesDegrees = getSectorAngles(rigid_slider.val, poly_slider.val, "foschi")
    sectorAngleRadians = [0,0,0,0]
    for i,sa in enumerate(sectorAnglesDegrees):
        sectorAngleRadians[i] = math.radians(sa)
    # 1. calculate min and max height
    minH = getMinH(a,b,c)
    maxH = getMaxH(a,b,c)
    hData = []
    tData = []
    rData = []
    hData = distributeH(minH, maxH, iterations)
    hData.sort()
    for h in hData:
        theta0 = getTheta0(a,b,c,h)
        rA, rA_ = getRigidKinematicAngle(sectorAngleRadians, theta0)
        tData.append(theta0)
        rData.append(math.degrees(rA_))
    return hData, tData, rData

def getAngles(a,b,c,h):
    # equation 1
    d = getD(h,c)
    print ("d", d)
    if (d >= a+b):
        print ("d is longer")
        costhetaA = 1
        thetaH = math.degrees(math.acos(c/(a+b)))
    else:
        # equation 2
        thetaH = math.degrees(math.acos(c/d))
        # equation 3
        costhetaA = ( math.pow(d,2) + math.pow(b,2) - math.pow(a,2) )/(2*d*b)
        print ("d", d, "a+b", a+b, "cosø", costhetaA, "øh", thetaH)
    
    if costhetaA < -1:
        costhetaA = -1
    print ("costhetaA", costhetaA)
    thetaA = math.degrees(math.acos(costhetaA))
    theta0 = 180 - thetaH - thetaA

    #print ("theta0", h, theta0)
    return theta0, thetaH, thetaA    
    
def getTheta0(a,b,c,h):
    # equation 1
    d = getD(h,c)
    #print("getTheta0", a, b, c, d, h)
    if d > 0:
        if (d >= a+b):
            #print "d is longer"
            costhetaA = 1
            thetaH = math.degrees(math.acos(c/(a+b)))
        else:
            # equation 2
            thetaH = math.degrees(math.acos(c/d))
            # equation 3
            costhetaA = ( math.pow(d,2) + math.pow(b,2) - math.pow(a,2) )/(2*d*b)
            #print "d", d, "a+b", a+b, "cosø", costhetaA, "øh", thetaH
        if costhetaA < -1:
            costhetaA = -1
        thetaA = math.degrees(math.acos(costhetaA))
        theta0 = 180 - thetaH - thetaA
        return theta0
    else:
         return 0    
    

# Define an action for modifying the line when any slider's value changes
def rigid_changed(val):
    global b_value
    heightData, thetaData, rigidData = getGraphData(a_slider.val,b_value,c_slider.val,rigid_slider.val,points)
    zeroHValue = getZeroH(a_slider.val,b_value,c_slider.val)
    minH = getMinH(a_slider.val,b_value,c_slider.val)
    maxH = getMaxH(a_slider.val,b_value,c_slider.val)
    rididPlot.set_xdata(rigidData)
    thetaPlot.set_xdata(thetaData)
    rididPlot.set_ydata(heightData)
    thetaPlot.set_ydata(heightData)
    zeroHLine.set_ydata([zeroHValue,zeroHValue])
    minHLine.set_ydata([minH,minH])
    maxHLine.set_ydata([maxH,maxH])
    # text updates
    a1, a2, a3, a4 = getSectorAngles(rigid_slider.val, poly_slider.val, "foschi")
    angletitle = r"Thysan-ori $\alpha_{1}$ %s, $\alpha_{2}$ %s, $\alpha_{3}$ %s, $\alpha_{4}$ %s" % (a1,a2,a3,a4)
    ax.set_title (angletitle)
    decimalplaces = 2
    linkagetitle = "a: %s b: %s c: %s" % ( round(a_slider.val,decimalplaces), round(b_value, decimalplaces), round(c_slider.val,decimalplaces))
    linkage_text.set_text(linkagetitle)
    zeroH_text.set_text(round(zeroHValue, decimalplaces))
    zeroH_text.set_y(zeroHValue-1.5)
    minH_text.set_text(round(minH, decimalplaces))
    minH_text.set_y(minH-1.5)

    rigid_high.set_text(round(max(rigidData),2))
    rigid_low.set_text(round(max(rigidData),2))

    rigid_high.set_x(max(rigidData)+5)
    rigid_high.set_y(maxH-4)
    rigid_low.set_x(min(rigidData))
    rigid_low.set_y(minH+1.7)

    rigidRange = round(max(rigidData) - min(rigidData), decimalplaces)
    rigidRange_str = r"Rigid range: %s $^\circ$" % (rigidRange)
    rangeR_text.set_text(rigidRange_str)    
    hRange = round(maxH-minH, decimalplaces)
    hRange_str = r"$h$ range: %s" % (hRange)
    rangeH_text.set_text(hRange_str)

    # zimmerman check
    print ("is this vertex rigid", ZimmermanRigidCheck (rigid_slider.val, poly_slider.val))
    print (abs(a_slider.val - b_value), abs(a_slider.val - b_value) - c_slider.val)
    fig.canvas.draw_idle()

def a_changed(val):
     global b_value
     b_slider.set_val(100 - val)
     b_value = 100-val
     #b_text.set_text("b: {:.2f}".format(b_value))
     rigid_changed(0)

# SET UP THE PLOT
axis_color = 'lightgrey'

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)

# Adjust the subplots region to leave some space for the sliders and buttons
fig.subplots_adjust(left=0.25, bottom=0.25)

# positioning variables for sliders
x1 = 0.25
x2 = 0.65
r1 = 0.12
r2 = 0.08
r3 = 0.04
s_w = 0.25
s_h = 0.03

# Add two sliders for tweaking the parameters
# Define an axes area and draw a slider in it
rigid_slider_ax  = fig.add_axes([x1, r1, s_w, s_h], facecolor="k")
rigid_slider = Slider(rigid_slider_ax, 'rigid', 0, 60, valinit=30, valstep=5, color="red")

poly_slider_ax  = fig.add_axes([x2, r1, s_w, s_h], facecolor="k")
poly_slider = Slider(poly_slider_ax, 'polygon', 3, 10, valinit=3, valstep=1, color="red")

a_slider_ax  = fig.add_axes([x1, r2, s_w, s_h])
a_slider = Slider(a_slider_ax, 'A', 0, 100, valinit=60, valstep=1, color="blue")

b_slider_ax  = fig.add_axes([x2, r2, s_w, s_h])
b_slider = Slider(b_slider_ax, 'B', 0.0, 100, valinit=40, color="grey")
#b_text = fig.text(x1+0.32,r2+0.01, "b: 40")
b_slider.active = False

c_slider_ax  = fig.add_axes([x1, r3, s_w, s_h], facecolor="k")
c_slider = Slider(c_slider_ax, 'C', -100, 100, valinit=0, color="blue")

rigid_slider.on_changed(rigid_changed)
a_slider.on_changed(a_changed)
#b_slider.on_changed(rigid_changed)
c_slider.on_changed(rigid_changed)
poly_slider.on_changed(rigid_changed)

# Add a button for resetting the parameters
reset_button_ax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
def reset_button_on_clicked(mouse_event):
    rigid_slider.reset()
    a_slider.reset()
    c_slider.reset()
    poly_slider.reset()

save_button_ax = fig.add_axes([0.7, 0.025, 0.1, 0.04])
save_button = Button(save_button_ax, 'Save', color=axis_color, hovercolor='0.975')
def save_button_on_clicked(mouse_event):
    a1, a2, a3, a4 = getSectorAngles(rigid_slider.val, poly_slider.val)
    filename = "figures/thysan-ori-plot_poly_%s_a1_%s_a2_%s_a3_%s_a4_%s_a_%s_b_%s_c_%s.png" % (poly_slider.val, a1,a2,a3,a4, a_slider.val, b_value, c_slider.val)
    fig.savefig(filename)
    filename = "figures/thysan-ori-plot_poly_%s_a1_%s_a2_%s_a3_%s_a4_%s_a_%s_b_%s_c_%s.svg" % (poly_slider.val, a1,a2,a3,a4, a_slider.val, b_value, c_slider.val)
    fig.savefig(filename)
    fig.canvas.draw_idle()

reset_button.on_clicked(reset_button_on_clicked)
save_button.on_clicked(save_button_on_clicked)

# calculate for the first run
a = a_slider.val
b_value = 100 - a_slider.val
b = b_value
b_slider.set_val(b)
c = c_slider.val

rigidAngle = rigid_slider.val
points = 1000

xlims = [-180, 180]

heightData, thetaData, rigidData = getGraphData(a,b,c,rigidAngle,points)

zeroHValue = getZeroH(a,b,c)
minH = getMinH(a, b, c)
maxH = getMaxH(a, b, c)

# Draw the initial plot
# The 'line' variable is used for modifying the line later

[rididPlot] = ax.plot(rigidData, heightData, linewidth=2, color='r', label="rigid angle")
[thetaPlot] = ax.plot(thetaData, heightData, linewidth=2, color='b', label=r"$\theta$ of linkage")
[zeroHLine] = ax.plot(xlims, [zeroHValue, zeroHValue], linewidth=1, color='k', linestyle=':', label="zero line")
[minHLine]  = ax.plot(xlims, [minH, minH], linewidth=1, color='k', linestyle='--', label="min line")
[maxHLine]  = ax.plot(xlims, [maxH, maxH], linewidth=1, marker='+', color='k', label="max line")

decimalplaces  = 2
linkagetitle   = "a: %s b: %s c: %s" % ( round(a_slider.val,decimalplaces), round(b_value, decimalplaces), round(c_slider.val,decimalplaces))
linkage_text   = ax.text(173,10, s=linkagetitle, bbox=dict(boxstyle="square", fc="w", ec="k"), ha="right")
zeroH_text     = ax.text(182,zeroHValue-1.5,s=round(zeroHValue, decimalplaces), ha="left")
minH_text      = ax.text(182,minH-1.5,s=round(minH, decimalplaces), ha="left")
rigid_high     = ax.text(max(rigidData)+5,maxH-4,s=round(max(rigidData), decimalplaces), bbox=dict(boxstyle="square", fc="w", ec="r"), ha="left")
rigid_low      = ax.text(min(rigidData),minH+1.7,s=round(min(rigidData), decimalplaces), bbox=dict(boxstyle="square", fc="w", ec="r"), ha="right")
rigidRange     = round(max(rigidData) - min(rigidData), decimalplaces)
rigidRange_str = r"Rigid range: %s $^\circ$" % (rigidRange)
rangeR_text    = ax.text(173,3,s=rigidRange_str, bbox=dict(boxstyle="square", fc="w", ec="r"), ha="right")
hRange         = round(maxH-minH, decimalplaces)
hRange_str     = r"$h$ range: %s" % (hRange)
rangeH_text    = ax.text(173,17,s=hRange_str, bbox=dict(boxstyle="square", fc="w", ec="b"), ha="right")

ax.set_xlim([-180, 180])
ax.set_ylim([0, 100])
ax.grid(True)
ax.set_xlabel("angle in degrees")
ax.set_ylabel(r"$h$ distance between plate")
ax.legend()

plt.show()



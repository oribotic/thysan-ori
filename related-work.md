# Related work

## Rigid Degree-Four Vertex in Origami

Zimmermann, Luca & Stanković, Tino. (2019). Rigid and Flat Foldability of a Degree-Four Vertex in Origami. Journal of Mechanisms and Robotics. 12. 1-18. 10.1115/1.4044737. 
Source: https://asmedigitalcollection.asme.org/mechanismsrobotics/article-abstract/12/1/011004/960558/Rigid-and-Flat-Foldability-of-a-Degree-Four-Vertex

the authors define the concise sector angle conditions with Equation 8. (shown in this paper as Equation @rigid) for rigid degree-four vertices including a _driving crease_. 

$$\mid \alpha_{1} - \alpha_{4} \mid \quad\geq\quad \mid \alpha_{2} - \alpha_{3} \mid$$

## Kinematics of Degree-Four Vertex in Origami

Foschi, R., Hull, T. C., & Ku, J. S. (2022). Explicit kinematic equations for degree-4 rigid origami vertices, Euclidean and non-Euclidean. Physical Review E, 106(5), 055001.
Source: https://arxiv.org/pdf/2206.12691

Equation 6. used to calculate another folding angle in a rigid-degree-4 origami vertex

$\tan{\frac{\rho_{1}}{2}$

**inputs**: sector angles $[\alpha_{1},\alpha_{2},\alpha_{3},\alpha_{4}]$ of the degree-4 rigid origami vertex, $\rho_{4}$ dihedral angle of the driving crease, 

**outputs**: $\pm \rho_{1}$

The equation is broken down into small chunks in code:

$e1 = 2\sin(\alpha_{1})\sin(\alpha_{2})\tan(\frac{\rho_{4}}{2})$

$e2 = 4\sin^2(\alpha_{1})\sin^2(\alpha_{3})\tan^2(\frac{\rho_{4}}{2}) - (\cos(\alpha_{2}) - \cos(\alpha_{1} - \alpha_{3} - \alpha{4})  +  (\cos(\alpha_{2}) - \cos(\alpha_{1} + \alpha_{3} - \alpha{4}))\tan^2(\frac{\rho_{4}}{2}))(\cos(\alpha_{2}) - \cos(\alpha_{1} + \alpha_{3} + \alpha_{4}) + (\cos(\alpha_{2}) - \cos(\alpha_{1} - \alpha_{3} + \alpha_{4}))\tan^2(\frac{\rho_{4}}{2}))$

$e3 = \cos(\alpha_{2}) - \cos(\alpha_{1} - \alpha_{3} - \alpha{4})  + (\cos(\alpha_{2}) - \cos(\alpha_{1} + \alpha_{3} - \alpha{4}) )\tan^2(\frac{\rho_{4}}{2})$

$\rho_{+} = e1 \cdot \sqrt{\frac{e2}{e3}}$

$\rho_{-} = -e1 \cdot \sqrt{\frac{e2}{e3}}$

in python:

```
def getRigidKinematicAngle (sectorAngles, pDegrees):
    # p = angle in radians
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
```

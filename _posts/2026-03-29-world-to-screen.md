---
layout: post
title:  "World to Screen"
date:   2026-03-29 19:33:05 +0100
categories: maths opengl graphics programming
permalink: /world-to-screen/
---
matrix multiplication is row by column 

if k x i = j and j is 0,1,0 then you use right hand rule to determine basis vectors and their directions

$$
\begin{vmatrix}
a&b
\\
c&d
\end{vmatrix}
^{-1}
=
\frac{1}{ad-bc}
\begin{vmatrix}
d&-b
\\
-c&a
\end{vmatrix}

$$
rotation around x is the pitch and rotation around the y axis is the yaw
soh cah toa

imagine a cuboid that contains the direction vector as it's diagonal from bottom origin corner to top opposite-origin corner. if you move yaw and pitch then the cuboid scales and moves about (as it contains the origin vector)

then do cross product of 
direction vector x up vector
then do cross vector of
left vector x direction vector to get the up vector actually perpendicular as currently it only exists in the perpendicular plane
ixj = k
kxi = j

projection matrix transformation is geometrically: objects within a frustum getting pulled in and normalised to [-1, 1], stuff further away becomes smaller.

view space > projection matrix multiplication > clip space > de-homogonize > ndc

Good resource on the overall OpenGL [pipeline][OpenGL-transform]

[OpenGL-transform]: https://www.songho.ca/opengl/gl_transform.html

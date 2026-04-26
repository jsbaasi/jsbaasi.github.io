---
layout: post
title:  "World to Screen"
date:   2026-03-29 19:33:05 +0100
categories: maths opengl graphics programming
permalink: /world-to-screen/
---
# Pre-amble
# Terms to parse differently than expected
`Space` - a set of co-ordinate axes. A point will need a change-of-basis transformation to move from one distinct space to another.
`Origin` - (0,0,0) in a co-ordinate space

I recommend 3blue1brown videos on linear algebra, your goal is to get an intuitive understanding of matrices, vectors and common transformations so you can imagine some of the transformations below in your head and work through your own problems
# Model space
Our journey begins with objects in their own "space". For each object, it lives in a space whose axes puts the object at the origin point, and other objects arrayed around it.

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

projection matrix + w divide sends each 3d point to the 2d location where the ray from that 3d point to the camera origin crosses a plane perpendicular to the view axis (-z in the case of opengl) then rescales to ndc (-1, 1)

# row-major vs column-major
column-major (opengl and vulkan default) is better for shaders and row-major (directx default) is better for cpu cache line apparently

$$
\begin{vmatrix}
a&b&c&d
\\
e&f&g&h
\\
i&j&k&l
\\
m&n&o&p
\end{vmatrix}
$$

it's a way to decide which way we want to flatten our matrix into a 1d memory array, keeping the columns contiguous
$$
a,e,i,m || b,f,j,n || c,g,k,o || d,h,l,p
$$
OR keeping the rows contiguous
$$
a,b,c,d || e,f,g,h || i,j,k,l || m,n,o,p
$$
glm maths library mimics glsl vec/matrix maths, [some info here](https://www.c-jump.com/bcc/common/Talk3/Math/GLM/GLM.html) and thus the api for manipulating objects is column major, e.g. mat\[0]\[3] is the same as mat.first_column.w

Good resource on the overall OpenGL [pipeline][OpenGL-transform]

[OpenGL-transform]: https://www.songho.ca/opengl/gl_transform.html

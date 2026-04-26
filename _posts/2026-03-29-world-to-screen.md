---
layout: post
title:  "World to Screen"
date:   2026-03-29 19:33:05 +0100
categories: maths opengl graphics programming
permalink: /world-to-screen/
---
# Pre-amble
## Terms to parse differently than expected
`Space` - a set of co-ordinate axes. A point will need a change-of-basis transformation to move from one distinct space to another.
`Origin` - (0,0,0) in a co-ordinate space
`Creator` - the entity that made the choices on the following matters:
- which co-ordinate convention to use (opengl vs directx), and thus which directions each of the conventional vectors, $\hat{i}$, $\hat{j}$, $\hat{k}$, will represent
- where the origin point is in the world space
- where to put items relative to each other
- what field-of-view angle to use for our perspective viewing on objects
- where to define the near + far + left + right + top + bottom for the perspective frustum
## Recommended reading
I recommend 3blue1brown videos on linear algebra, your goal is to get an intuitive understanding of matrices, vectors and common transformations so you can imagine some of the transformations below in your head and work through your own problems
# Intro
I learnt some of this stuff as part of an esp I made for assault cube, source can be found at [achack](https://github.com/jsbaasi/achack). I thought it would be helpful for myself to condense some of my linear algebra learnings into this write-up, targeting 3d-space-to-2d-screen transformations that a game developer may use.

Hopefully others find this useful but, disclaimer, I am not a mathematician or a graphics programmer, just some dude. If you have any comments/questions/corrections or would like to just talk, please reach me through `jsbaasi at stormblessed dot fr` or `jsbaasi` on Discord.
# Model space
Our journey begins with objects in their own "space". For each object, it lives in a space whose axes describe the object as being at the origin point (0,0,0).

Simple so far.
# Model space to World space
Each object goes through a change-of-basis + translation to be put into the world space. It is now in a space with other objects.
# World space to View space
A camera now comes into the mix, it's also an object in world space. We need to pick a point to view space from, this point is where we'll put the camera. Next we ask ourselves, how do we note where the camera is looking?

We can do with 3 basis vectors. One to describe what up and down means for the camera, one to describe what left and right means for the camera, and one to describe what forwards and backwards means for the camera. $\hat{i}$, $\hat{j}$, $\hat{k}$. 

For example, I have placed my camera at (3,3,3). It is looking at the origin. It's forward vector will be origin - (3,3,3) which is (-3,-3,-3). These forward, up, right vectors are special and known as basis vectors. They are stored as unit vectors for convention I guess, so must be normalised. Forward becomes 
 $$\vec{forward} = \frac{1}{\sqrt27} \begin{pmatrix} -3 \\ -3 \\ -3 \end{pmatrix}$$
If we don't care about roll (like fps games), then we set $\vec{up}$ to $\begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}$, calculate the cross-product between $\vec{forward}$ and $\vec{up}$ to get $\vec{right}$ if we're in right-handed convention or $\vec{left}$ otherwise. Then calculate the cross product between $\vec{right}$ and $\vec{forward}$ to set the real $\vec{up}$ and not just some vector that occupies the up plane. We can generate these bases from:
- the point we're looking at as I have worked through above, if you're decided on what you want the camera to look at
- euler angles if you're starting your working out from your self, deciding what yaw, pitch and roll you have (angles rotated around the world space basis vectors) then generating the bases vectors through trigonometry from those angles
- quaternions, which I don't know much about
- maybe some others?
## Deriving the transformation matrix for world-to-view
We have the basis vectors of the camera and it's position within the world space.

In the view space the camera is at the centre, thus we can imagine to move the camera itself from the world space to view space we first translated it to the origin, then rotated it to face whichever axis we determined to be the forward vector (this is sometimes opposite, where the camera is rotated to face the opposite direction of where it's looking at)

We need homogenous co-ordinates to describe a translation in a matrix multiplication, otherwise we'd need to do two operations. Your choice whether you want to go to the fourth dimension or more maths.

So the final matrix will be the opposite of it's current position THEN the opposite of the rotation the camera had. So when other objects are transformed by this matrix, they are translated away to the same distance and rotated to keep the same orientation relative to whatever rotations the camera had.
# View space to Clip space
We now have to decide:
1. what's in our field of view
2. if you're doing perspective projection (objects further away are smaller) as opposed to orthogonal projection (objects are same size everywhere) then what is the dimensions of each object when we've applied our perspective projection to it.
## 1.
We do this by geometrically describing a box (if orthogonal) or frustum (if perspective) in the direction that the camera is facing. Objects outside of this projection are "clipped". Practically this means we compare whether the position components of the object meet the following $-w <= x,y,z <= w$ criteria after the projection matrix multiplication
## 2.
We do this by geometrically describing a frustum. Objects within this frustum gets mapped to a cube co-ordinate space constrained at [-1, 1]. Thus, objects at the back of the frustum will under-go a greater compression compared to objects that are closer to the front.

## Deriving the transformation matrix for view-to-clip
This one is a bit trickier but we can arrive to the optimised version that everyone has agreed on by summarising our motivations for each of the components:
### X and Y
- Need to determine relationship between x,y and z because of our requirement that objects further away will be smaller
- Need to constrain $left< x < right$ and $bottom < y < top$ based on the values we chose for our projection
- Imagine a ray travelling from the 3d point to the camera (origin point in the view space). where this ray crosses the near plane (the screen essentially) will determine the relationship between $x,y$ and $z$ e.g. for $x$: $$\frac{x_{view}}{z_{view}}=\frac{x_{ndc}}{near}$$$$x_{ndc}=\frac{near*x_{view}}{z_{view}}$$
- Objects at the far/left/bottom boundaries of the projection will be mapped to -1 on the respective axis && objects at the near/left/bottom boundaries of the projection will be mapped to -1 on the respective axis in NDC space
- It is agreed on to split projection transform and perspective divide in world-to-screen formulae, so if we do have formulae for view > NDC then factor out the divide-by-z to get the transformation between view > clip then we can arrive at NDC at our choosing by perspective dividing (one reason we do this is that we can check if an object is outside of clip space at this point)
- We can encapsulate all of this information by modelling it as finding the equation of a line.
- E.g. for $x$ draw a graph with $x_{ndc}$ axis, -1 to 1 and $x_{view}$ axis, far and near. With the 2 points (-1, near) and (1, far) we can determine the gradient
- Substitute in the above relationship between $x,y$ and $z$ to get the intercept constant for the line equation. Re-arrange so we have a common denominator of z.
This decides our $x,y$ components of projection transform
### Z
- $z$ has no relationship on $x,y$, just 
# NDC space
# Screen space
Great, we made it.


















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

---
layout: post
title: World to Screen
date: 2026-03-29 19:33:05 +0100
categories: maths opengl graphics programming
permalink: /world-to-screen/
---
- [Pre-amble](#pre-amble)
	- [Terms to parse differently than expected (maybe)](#terms-to-parse-differently-than-expected-maybe)
	- [Recommended pre/post actions](#recommended-prepost-actions)
		- [Pre](#pre)
		- [Post](#post)
- [Intro](#intro)
- [Model space](#model-space)
- [Model space to World space](#model-space-to-world-space)
- [World space to View space](#world-space-to-view-space)
	- [Deriving the transformation matrix for world-to-view](#deriving-the-transformation-matrix-for-world-to-view)
- [View space to Clip space](#view-space-to-clip-space)
	- [1.](#1)
	- [2.](#2)
	- [Deriving the transformation matrix for view-to-clip](#deriving-the-transformation-matrix-for-view-to-clip)
		- [X and Y](#x-and-y)
		- [Z](#z)
		- [W](#w)
- [Clip space to NDC space](#clip-space-to-ndc-space)
	- [transformation for clip-to-ndc](#transformation-for-clip-to-ndc)
- [Screen space](#screen-space)
	- [transformation for ndc-to-screen](#transformation-for-ndc-to-screen)
- [Conclusion](#conclusion)
- [Misc](#misc)
	- [Row-major vs Column-major](#row-major-vs-column-major)
	- [Radians and degrees](#radians-and-degrees)
	- [Pre- vs post- multiply](#pre--vs-post--multiply)

# Pre-amble
## Terms to parse differently than expected (maybe)
`Space` - a set of co-ordinate axes. A point will need a change-of-basis transformation to move from one distinct space to another.
`Origin` - (0,0,0) in a 3-dimensional co-ordinate space
`Creator` - the entity that made the choices on the following matters:
- which co-ordinate convention to use (opengl vs directx), and thus which directions each of the conventional vectors, $\hat{i}$, $\hat{j}$, $\hat{k}$, will represent
- where the origin point is in the world space
- where to put items relative to each other
- what field-of-view angle to use for our perspective viewing on objects
- where to define the near + far + left + right + top + bottom for the perspective frustum

`Translation` - could be used to mean moving between spaces but this write-up it only means moving an object's position, done through matrix multiplication ONLY by using homogeneous co-ordinates
`NDC` - these letters parse to abbreviation normalised device co-ordinates
`Clip` - the space where we decide what's inside/outside of our field of view. When used for it's common meaning e.g. clipping a hedge, the word will be accompanied by quotation marks
`View` - used interchangeably to mean view space, the space titled view and view, as in what's in your vision
`Components` - components of a vector e.g. $x,y,z$ of a 3-dimensional vector
`Position` - interchangeably used to mean vector, a point in space
## Recommended pre/post actions
### Pre
I recommend 3blue1brown videos on linear algebra, your goal is to get an intuitive understanding of matrices, vectors and common transformations so you can imagine some of the transformations below in your head. Think of the below:
- what does a matrix mean
- matrix multiplication, vector multiplication
- determinant of matrix
- change-of-basis
- dot product
- cross product

Skim the 3 https://learnopengl.com/Getting-started chapters `Transformations` to `Camera` to see some of the pictures

https://www.songho.ca/opengl/files/gl_camera02.gif this is a visualisation of world-to-view, haven't found one for projection _yet_
### Post
Implement something that touches upon every stage of this imaginary world to monitor pipeline. Camera implementation as is implemented in the OpenGL online book. Alternatively using a library like SDL or raylib to skip learning the OpenGL API for the GPU as it's quite explicit to speak and isn't relevant to the world-to-screen pipeline ideas. Here's mine https://github.com/jsbaasi/camcpu that is buggy (doesn't clip) at the time of writing.

Look at other explanations of the world-to-screen pipeline to form your own _perspective_. Overall [pipeline](OpenGL-transform) as described by Song Ho Ahn, brilliant resources from them.
# Intro
I learnt some of this stuff as part of an esp I made for assault cube, source can be found at [achack](https://github.com/jsbaasi/achack). I thought it would be helpful for myself to condense some of my linear algebra learnings into this write-up, targeting 3d-space-to-2d-screen transformations that a game developer may use.

Hopefully others find this useful but, disclaimer, I am not a mathematician or a graphics programmer, just some dude. If you have any questions or would like to discuss further, please reach me through `jsbaasi at stormblessed dot fr` or `jsbaasi` on Discord. If there any corrections to make, please open an MR on [github](https://github.com/jsbaasi/jsbaasi.github.io)
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
- Euler angles if you're starting your working out from your self, deciding what yaw, pitch and roll you have (angles rotated around the world space basis vectors) then generating the bases vectors through trigonometry from those angles
	- Imagine a cuboid that contains the direction vector as it's diagonal from bottom origin corner to top opposite-origin corner. if you move yaw and pitch then the cuboid scales and moves about (as it contains the origin vector)
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
2. if you're doing perspective projection (objects further away are smaller) as opposed to orthographic projection (objects are same size everywhere) then what is the dimensions of each object when we've applied our perspective projection to it.
3. what co-ordinate conventions we are living by e.g. if it's OpenGL we look down $-z$, but conventionally $z_{near}$ and $z_{far}$ are given as positive values so we must negate $z$ at some point

## 1.
We do this by geometrically describing a box (if orthographic) or frustum (if perspective) in the direction that the camera is facing. Objects outside of this projection are "clipped". Practically this means we compare whether the position components of the object meet the following $-w <= x,y,z <= w$ criteria after the projection matrix multiplication
## 2.
We do this by geometrically describing a frustum. Objects within this frustum gets mapped to a cube co-ordinate space constrained at [-1, 1]. Thus, objects at the back of the frustum will under-go a greater compression compared to objects that are closer to the front.

## Deriving the transformation matrix for view-to-clip
This one is a bit trickier but we can arrive to the optimised version that everyone has agreed on by summarising our motivations for each of the components, working row by row of the final matrix, setting 0s where there's no relationship *between* the components. Obviously you can decide your own route of getting from view to clip to NDC. Such an exercise may help you understand the decisions that were made as opposed to e.g. dropping to 3 dimensions after the translation in world-to-view transformation or not being in 4 dimensions at all and having to do translation in a separate operation.
### X and Y
- Need to determine relationship between x,y and z because of our requirement that objects further away will be smaller
- Need to constrain $left< x < right$ and $bottom < y < top$ based on the values we chose for our projection
- Imagine a ray travelling from the 3d point to the camera (origin point in the view space). where this ray crosses the near plane (the screen essentially) will determine the relationship between $x,y$ and $z$ e.g. for $x$:
$$\frac{x_{view}}{z_{view}}=\frac{x_{ndc}}{near}$$
$$x_{ndc}=\frac{near*x_{view}}{z_{view}}$$
- Objects at the far/left/bottom boundaries of the projection will be mapped to -1 on the respective axis && objects at the near/left/bottom boundaries of the projection will be mapped to -1 on the respective axis in NDC space
- It is agreed on to split projection transform and perspective divide in world-to-screen formulae, so if we do have formulae for view > NDC then factor out the divide-by-z to get the transformation between view > clip then we can arrive at NDC at our choosing by perspective dividing (one reason we do this is that we can check if an object is outside of clip space at this point)
- We can encapsulate all of this information by modelling it as finding the equation of a line.
- E.g. for $x$ draw a graph with $x_{ndc}$ axis, -1 to 1 and $x_{view}$ axis, far and near. With the 2 points (-1, near) and (1, far) we can determine the gradient
- Substitute in the above relationship between $x,y$ and $z$ to get the intercept constant for the line equation. Re-arrange so we have a common denominator of z.
	This decides our $x,y$ components of projection transform

### Z
- $z$ has no relationship on $x,y$ to work in, just constraints placed by the frustum/box so the $(z_{view},z_{ndc})$ relation, mapping $(near,-1)$ and $(far,1)$.
- Again we model it as a graph problem and substitute in the above points
- We have 2 variables in our equation and we can't use $x,y$ slots, as there's no relation, but $w$ is always 1 in view space so we can use that slot as a hack. I don't think it means anything geometrically but correct me if wrong. This is what I mean by "optimised" version, there is decisions baked into this method that are counter-intuitive to suggest but can be recognised as optimal after understanding

### W
- $z$ is needed for deciding what order the objects are seen in e.g. which object is at the front so all objects that are obscured by it don't need to be drawn, saving time in our draw loop && for perspective divide, so if we want to do this in one operation we need to save the $z$ value somehow
- We use this row of the transformation to save the z value for the perspective divide later. So this final row is just $0,0,1,0$
I recommend thinking through the above motivations and then looking at this [derivation](https://www.songho.ca/opengl/gl_projectionmatrix.html) of the projection matrices (orthographic and perspective)
# Clip space to NDC space
Normalised device co-ordinates. By being here we have carried forward all the above transformations to our objects that make them look 2d down the forward axis. Being normalised means we're understandable by all hardware/graphics APIs, so we can pass off our work to a library at this point but as we've come so far we might as well make the next jump to screen space and decide where exactly to draw the pixel.
## transformation for clip-to-ndc
View > clip > NDC transformations are setup so we just perspective divide at this point and narrow to 3-dimensions if we want to stay.  Huge commitment
# Screen space
Great, we made it.
## transformation for ndc-to-screen
- It's a range map from `[-1,1]` to e.g. `[0,799]` if you have 800 pixel width/height. Do this for both $x$ and $y$.

# Conclusion
| Model space |
      | model matrix
      ↓
| World space |
      | view matrix
      ↓
| View space |
      | projection matrix
      ↓
| Clip space |
      | de-homogenize
      ↓
| NDC space |
      | range map
      ↓
| Screen space |
# Misc
## Row-major vs Column-major
Column-major (opengl and vulkan default) is better for shaders and row-major (directx default) is better for cpu cache line apparently

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
glm maths library mimics glsl vec/matrix maths, [some info here](https://www.c-jump.com/bcc/common/Talk3/Math/GLM/GLM.html) and thus the api for manipulating objects is column major, e.g. mat\[0]\[3] is the same as my_matrix.first_column.w_component
## Radians and degrees
GLM functions expect angles to be given in radians, so wrap your angles in `glm::radians()`
## Pre- vs post- multiply
GLM functions like `glm::translate(input_matrix, translation_vector)` post-multiply meaning the `translation_vector` is multiplied to the _right_ of the `input_matrix` like `input_matrix * translation_vector`. So if you wanted to apply a rotation to an object around the object's $up$ axis then I would build it like `translation_from_origin * rotation_around_up * translation_to_origin` and in GLM calls it would look like:
```
glm::translate(input_matrix, translation_to_origin);
glm::translate(input_matrix, rotation_around_up);
glm::translate(input_matrix, translation_from_origin);
```
Something to stay aware of.
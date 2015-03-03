Reference
=========

Drawing
-------

### Entity
Not instantiable (i.e. you cannot use it) but it is subclassed by polygons,
imgages and other not-yet-implemented classes.

The creation of an entity is a resource expensive operation, better to make it
at loading time, outside the drawing functions

__Attributes__:
* `.r` radius
* `.x`, `.y`, `.z` position
* `.fill`, `.stroke` color

__Methods__:
* `draw()` draw the entity


### Polygon
```python
Polygon(n)
```
(Entity) Generates a new polygon class, with the given number of sides, and return an
instance.

To draw a square with side 1:
```python
p = Polygon(4)

def draw():
    p.r = 0.5
    p.draw()
    
```

### Frame
```python
Frame()
```
(Entity) Gets framebuffer from renderer window and displays it.


Coloring
--------

### rgb
```python
rgb(x)
```
Greyscale color

```python
rgb(x, a)
```
Greyscale color with alpha

```python
rgb(r, g, b)
```
RGB components

```python
rgb(r, g, b, a)
```
RGB components with alpha


### hsv
```python
hsv(h)
```
Just hue component

```python
hsv(h, a)
```
Just hue component with alpha

```python
hsv(h, s, v)
```
HSV components

```python
hsv(h, s, v, a)
```
HSV components with alpha


### strokeWeight
```python
strokeWeight(w)
```
Stroke weight in pixels


Transforming
------------

### push
### pop
### popmatrix
### scale
### rotate
### rotateX
### rotateY
### rotateZ
### translate
### turnaroud
### grid


Audio
-----


Other
-----

### time2rad
```python
time2rad(mul=1)
```  
Sometimes trigonometric functions don't handle really high numbers, this
returns `(mul*time()) % (2*pi)`

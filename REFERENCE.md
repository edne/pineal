Reference
=========

Graphic
-------

### Entity
Not instantiable (i.e. you cannot use it) but is subclassed by polygons, imgages
and other not-yet-implemented classes.

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
Generates a new polygon class, with the given number of sides, and return an
instance.

```python
p = Polygon(4)

def draw():
    p.r = 0.5
    p.draw()
    
```


Audio
-----



Other
-----

### time2rad
```python
time2rad(mult=1)
```  
Sometimes trigonometric functions don't handle really high numbers, this
returns `(mul*time()) % (2*pi)`

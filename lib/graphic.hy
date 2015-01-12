(import [pyglet.gl :as gl]
        [math])

(defclass GLEntity []
  [ [vertsGl None]

    [_generateVerts
      (with-decorator staticmethod (fn []))]

    [__init__ (fn [self]
      (setv self.r 1)
      (setv [self.x self.y self.z] [0 0 0])
      (setv self.c [1 1 1 1])
      None)]

    [draw (fn [self])]])


(defclass PolInt [GLEntity]
  [ [_generateVerts
      (with-decorator staticmethod (fn [c n]
        (setv verts [])
        (setv theta 0)
        (for [i (range n)]
          (.append verts 0)
          (.append verts 0)

          (.append verts (math.cos theta))
          (.append verts (math.sin theta))

          (+= theta (/ (* 2 math.pi) n))

          (.append verts (math.cos theta))
          (.append verts (math.sin theta)))

        (setv c.vertsGl (apply (* gl.GLfloat (len verts)) verts))))]

    [draw (fn [self]
      (gl.glTranslatef self.x self.y self.z)
      (gl.glScalef self.r self.r 1)

      (gl.glVertexPointer 2 gl.GL_FLOAT 0 self.vertsGl)

      (gl.glEnableClientState gl.GL_VERTEX_ARRAY)

      (apply gl.glColor4f self.c)
      (gl.glDrawArrays gl.GL_TRIANGLES 0 (len self.vertsGl))
      (gl.glTranslatef (- self.x) (- self.y) (- self.z)) )]])


(defn Polygon [n]
  (defclass PolClass [PolInt] [])
  (._generateVerts PolClass PolClass n)
  (PolClass))


(defmacro multidef [&rest margs]
  (defn nestle [funcs]
    (if funcs
      `(try
        (apply ~(get funcs 0) fargs)
        (except [TypeError]
          ~(nestle (slice funcs 1))))
      '(throw TypeError)))
  `(defn ~(get margs 0) [&rest fargs]
    ~(nestle (slice margs 1))))


(defn push [] (gl.glPushMatrix))
(defn pop [] (gl.glPopMatrix))


(multidef scale
  (fn [s] (gl.glScalef s s s))
  (fn [x y] (gl.glScalef x y 1))
  (fn [x y z] (gl.glScalef x y z)))


(multidef rotate
  (fn [angle]
    (gl.glRotatef
      (/ (* angle 180) math.pi)
      0 0 1)
  (fn [angle x y z]
    (gl.glRotatef
      (/ (* angle 180) math.pi)
      x y z))))

(defn rotateX [angle]
  (gl.glRotatef
      (* math.pi (/ angle 180))
      1 0 0))

(defn rotateY [angle]
  (gl.glRotatef
      (/ (* angle 180) math.pi)
      0 1 0))

(defn rotateZ [angle]
  (gl.glRotatef
      (/ (* angle 180) math.pi)
      0 0 1))

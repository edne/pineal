(import [pyglet.gl :as gl]
        [lib.windows [getFrame :as _getFrame]]
        [math])

(defclass _Entity []
  [ [vertsGl None]

    [_generateVerts
      (with-decorator staticmethod (fn []))]

    [__init__ (fn [self]
      (setv self.r 1)
      (setv [self.x self.y self.z] [0 0 0])
      (setv self.c [1 1 1 1])
      None)]

    [draw (fn [self])]])


(defclass _PolInt [_Entity]
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

      (apply gl.glColor4f (_color self.c))
      (gl.glDrawArrays gl.GL_TRIANGLES 0 (len self.vertsGl))
      (gl.glTranslatef (- self.x) (- self.y) (- self.z)) )]])


(defn Polygon [n]
  (defclass PolClass [_PolInt] [])
  (._generateVerts PolClass PolClass n)
  (PolClass))


(defclass _ImageText [_Entity]
  [ [__init__ (fn [self texture ratio]
      (.__init__ _Entity self)
      (setv self.texture texture)
      (setv self.ratio ratio)
      None)]

    [draw (fn [self]
      (setv w (* self.r self.ratio))
      (setv h self.r)
      (if self.texture
        (.blit self.texture
          (- self.x (/ w 2))
          (- self.y (/ h 2))
          self.z
          w h)))]])

(defclass _Frame [_ImageText]
  [ [draw (fn [self]
    (setv self.texture (_getFrame))
    (.draw _ImageText self))]])

(defn Frame [] (_Frame None (/ 4 3)))


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


(def _matrix_sp 0)

(defn push []
  (global _matrix_sp)
  (if (< _matrix_sp 30)
    (do
      (gl.glPushMatrix)
      (+= _matrix_sp 1)
    (gl.glLoadIdentity))))

;(defn pop [] (gl.glPopMatrix))
(defn pop []
  (global _matrix_sp)
  (if (> _matrix_sp 0)
    (do
      (gl.glPopMatrix)
      (-= _matrix_sp 1))
    (gl.glLoadIdentity)))


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


(multidef __color
  (fn [x]       [x x x 1])
  (fn [x a]     [x x x a])
  (fn [r g b]   [r g b 1])
  (fn [r g b a] [r g b a]))
(defn _color [c]
  (apply __color c))

(import [colorsys [hsv_to_rgb]])
(multidef hsv
  (fn [h]       (hsv_to_rgb h 1 1))
  (fn [h s v]   (hsv_to_rgb h s v))
  (fn [h s v a]
    (setv [r g b] (hsv_to_rgb h s v))
    [r g b a])
  (fn [h a] (hsv h 1 1 a)))

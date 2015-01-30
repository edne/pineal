(import [pyglet.gl :as gl]
        [pyglet.graphics [draw]]
        [lib.windows [getFrame :as _getFrame]]
        [math [cos sin pi]]
        [colorsys [hsv_to_rgb]])

(require hy.contrib.multi)

(defclass _Entity []
  [ [vertsGl None]
    [wVerts []]

    [_generateVerts
      (with-decorator staticmethod (fn []))]

    [__init__ (fn [self]
      (setv self.r 1)
      (setv [self.x self.y self.z] [0 0 0])
      (setv self.fill [1 1 1 1])
      (setv self.stroke [1 1 1 1])
      None)]

    [draw (fn [self])]])


(defclass _PolInt [_Entity]
  [ [_generateVerts
      (with-decorator staticmethod (fn [c n]
        (setv verts [])
        (setv theta (/ pi -2))
        (for [i (range n)]
          (.append verts 0)
          (.append verts 0)

          (.append verts (cos theta))
          (.append verts (sin theta))

          (+= theta (/ (* 2 pi) n))

          (.append verts (cos theta))
          (.append verts (sin theta)))

        (setv c.vertsGl (apply (* gl.GLfloat (len verts)) verts))

        (setv c.wVerts (flatten (map
          (fn [i]
            (setv theta (+ (/ pi -2) (* i (* 2 (/ pi n)))))
            [(cos theta) (sin theta)])
          (range n))))))]

    [draw (fn [self]
      (gl.glTranslatef self.x self.y self.z)
      (gl.glScalef self.r self.r 1)

      (gl.glVertexPointer 2 gl.GL_FLOAT 0 self.vertsGl)
      (gl.glEnableClientState gl.GL_VERTEX_ARRAY)

      (apply gl.glColor4f (_color self.fill))
      (gl.glDrawArrays gl.GL_TRIANGLES 0 (len self.vertsGl))

      (apply gl.glColor4f (_color self.stroke))
      (draw
        (// (len self.wVerts) 2) gl.GL_LINE_LOOP
        (tuple ["v2f" self.wVerts]))

      (gl.glTranslatef (- self.x) (- self.y) (- self.z)))]])


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
      (setv w (* 2 self.r self.ratio))
      (setv h (* 2 self.r))
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

(defn Frame [] (_Frame None 1))


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


(defmulti scale
  ([s] (gl.glScalef s s s))
  ([x y] (gl.glScalef x y 1))
  ([x y z] (gl.glScalef x y z)))


(defmulti rotate
  ([angle]
    (gl.glRotatef (/ (* angle 180) pi) 0 0 1))
  ([angle x y z]
    (gl.glRotatef (/ (* angle 180) pi) x y z)))

(defn rotateX [angle]
  (gl.glRotatef
      (* pi (/ angle 180))
      1 0 0))

(defn rotateY [angle]
  (gl.glRotatef
      (/ (* angle 180) pi)
      0 1 0))

(defn rotateZ [angle]
  (gl.glRotatef
      (/ (* angle 180) pi)
      0 0 1))


(defmulti translate
  ([x y] (gl.glTranslatef x y 0))
  ([x y z] (gl.glTranslatef x y z)))


(defmulti __color
  ([x]       [x x x 1])
  ([x a]     [x x x a])
  ([r g b]   [r g b 1])
  ([r g b a] [r g b a]))
(defn _color [c]
  (apply __color c))

(defmulti hsv
  ([h]       (hsv_to_rgb h 1 1))
  ([h s v]   (hsv_to_rgb h s v))
  ([h s v a] (+ (list (hsv_to_rgb h s v)) [a]))
  ([h a] (hsv h 1 1 a)))


(defn strokeWeight [weight]
  (gl.glLineWidth weight))

(import [pyglet.gl :as gl]
        [pyglet.graphics [draw]]
        [lib.windows [getFrame :as _getFrame]]
        [math [cos sin pi]]
        [lib.graphic.transforming [*]]
        [lib.graphic.coloring [*]])

(require hy.contrib.multi)


(defclass _Entity []
  [ [vertsGl None]
    [sVerts []]
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
        (setv c.sVerts (flatten (map
          (fn [i]
            (setv dtheta (* 2 (/ pi n)))
            (setv theta0 (* i dtheta))
            (setv theta1 (+ theta0 dtheta))
            [ 0 0
              (cos theta0) (sin theta0)
              (cos theta1) (sin theta1)])
          (range n))))

        (setv c.wVerts (flatten (map
          (fn [i]
            (setv theta (+ (/ pi -2) (* i (* 2 (/ pi n)))))
            [(cos theta) (sin theta)])
          (range n))))))]

    [draw (fn [self]
      (gl.glTranslatef self.x self.y self.z)
      (gl.glScalef self.r self.r 1)

      (apply gl.glColor4f (color self.fill))
      (draw
        (// (len self.sVerts) 2) gl.GL_TRIANGLES
        (tuple ["v2f" self.sVerts]))

      (apply gl.glColor4f (color self.stroke))
      (draw
        (// (len self.wVerts) 2) gl.GL_LINE_LOOP
        (tuple ["v2f" self.wVerts]))

      (gl.glScalef (/ 1 self.r) (/ 1 self.r) 1)
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

(import [pyglet.gl :as gl]
        [pyglet.graphics [draw vertex_list]]
        [lib.windows [getFrame :as _getFrame]]
        [math [cos sin pi]]
        [lib.graphic.transforming [*]]
        [lib.graphic.coloring [*]])

(require hy.contrib.multi)


(defn maxdepth [depth]
  "Decorator to set a maximum recursion limit"
  (defn decorator [f]
    (defn decorated [&rest args &kwargs kwargs]
      (if (in "depth" (.keys f.func_dict))
        (+= f.depth 1)
        (setv f.depth 0))
      (if (> f.depth depth)
        (setv f.depth 0)  ; reset the counter
        (apply f args kwargs)))))


(defclass _Entity []
  [ [vertsGl None]
    [n 4]
    [slist []]
    [wlist []]

    [_definePolygon
      (with-decorator staticmethod (fn []))]

    [__init__ (fn [self]
      (setv self.r 1)
      (setv [self.x self.y self.z] [0 0 0])
      (setv self.fill [1 1 1 1])
      (setv self.stroke [1 1 1 1])
      None)]

    [draw (fn [self])]])


(defclass _PolInt [_Entity]
  [ [_definePolygon
      (with-decorator staticmethod (fn [c n]
        (setv c.n n)))]

    [draw (fn [self]
      (gl.glTranslatef self.x self.y self.z)
      (gl.glScalef self.r self.r 1)

      (unless self.wlist
        (setv self.wlist
          (vertex_list self.n
            (tuple ["v2f/static" (flatten (map (fn [i]
              (setv theta (+ (/ pi -2) (* i (* 2 (/ pi self.n)))))
              [(cos theta) (sin theta)])
              (range self.n)))])
            (tuple ["c4f/stream" (* [1] 4 self.n)]))))

      (unless self.slist
        (setv self.slist
          (vertex_list (* self.n 3)
            (tuple ["v2f/static" (flatten (map (fn [i]
              (setv dtheta (* 2 (/ pi self.n)))
              (setv theta0 (* i dtheta))
              (setv theta1 (+ theta0 dtheta))
              [ 0 0
                (cos theta0) (sin theta0)
                (cos theta1) (sin theta1)])
            (range self.n)))])
            (tuple ["c4f/stream" (* [1] 4 (* self.n 3))]))))

      (setv self.wlist.colors (* (color self.stroke) self.n))
      (setv self.slist.colors (* (color self.fill) (* self.n 3)))

      (.draw self.slist gl.GL_TRIANGLES)
      (.draw self.wlist gl.GL_LINE_LOOP)

      (gl.glScalef (/ 1 self.r) (/ 1 self.r) 1)
      (gl.glTranslatef (- self.x) (- self.y) (- self.z)))]])


(defn Polygon [n]
  (defclass PolClass [_PolInt] [])
  (._definePolygon PolClass PolClass n)
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

(import
  [pyglet.gl :as gl]
  [pyglet.graphics [vertex_list]]
  [pyglet.image]
  [pyglet.image.codecs.png [PNGImageDecoder]]
  [lib.windows [getRenderTexture :as _getRenderTexture]]
  [math [cos sin pi]]
  [time [time]]
  [lib.graphic.transforming [*]]
  [lib.graphic.coloring [*]])

(require hy.contrib.multi)


(defun time2rad [&optional [mult 1]]
  "trigonometric functions don't handle really high numbers"
  (% (* mult (time)) (* 2 pi)))


(defclass _Entity []
  "
  Base class of drawing primitives
  "
  [[vertsGl None]
   [n 4]
   [solid-list []]
   [wired-list []]

   [_definePolygon
     (with-decorator staticmethod (fn []))]

   [__init__
     (fn [self]
         (setv self.fill
               [1 1 1 1])
         (setv self.stroke
               [1 1 1 1])
         None)]

   [draw
     (fn [self])]])


(defn build-wired-list [n]
  (vertex_list n
               (tuple ["v2f/static"
                       (flatten
                         (map (fn [i]
                                  (setv theta
                                        (-> (/ pi n)
                                            (* 2 i)))
                                  [(cos theta) (sin theta)])
                              (range n)))])
               (tuple ["c4f/stream"
                       (* [1] 4 n)])))


(defn build-solid-list [n]
  (vertex_list (* n 3)
               (tuple ["v2f/static"
                       (flatten
                         (map (fn [i]
                                  (setv dtheta
                                        (* 2 (/ pi n)))
                                  (setv theta0
                                        (* i dtheta))
                                  (setv theta1
                                        (+ theta0 dtheta))
                                  [ 0 0
                                    (cos theta0) (sin theta0)
                                    (cos theta1) (sin theta1)])
                              (range n)))])
               (tuple ["c4f/stream"
                       (* [1] 4
                          (* n 3))])))


(defclass _PolInt [_Entity]
  "
  Interface of polygon classes
  "
  [[_definePolygon
     (with-decorator staticmethod (fn [c n]
                                      (setv c.n n)))]

   [draw
     (fn [self]
         (unless self.wired-list
           (setv self.wired-list
                 (build-wired-list self.n)))

         (unless self.solid-list
           (setv self.solid-list
                 (build-solid-list self.n)))

         (setv self.wired-list.colors (* (color self.stroke)
                                         self.n))
         (setv self.solid-list.colors (* (color self.fill)
                                         (* self.n 3)))

         (.draw self.solid-list gl.GL_TRIANGLES)
         (.draw self.wired-list gl.GL_LINE_LOOP))]])


(defn Polygon [n]
  "
  Generates a new polygon class, with the given number of sides,
  and return an instance
  "
  (defclass PolClass [_PolInt] [])
  (._definePolygon PolClass PolClass n)
  (PolClass))


(defn blit [img]
  (.blit img
         -1 1 0
         2 -2))


(defn new-blittable [inner]
  (setv entity (_Entity))

  (defn draw []
      (blit inner))

  (setv entity.draw draw)
  entity)


(defn Frame []
  (setv frame (_Entity))

  (defn draw []
    (setv texture (_getRenderTexture))
    (when texture
      (blit texture)))

  (setv frame.draw draw)
  frame)


(defn Image [name]
  "
  Image from png file
  "
  (new-blittable (apply pyglet.image.load
                        [(+ "images/" name ".png")]
                        {"decoder" (PNGImageDecoder)})))

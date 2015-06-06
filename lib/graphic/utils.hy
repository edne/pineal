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


(defclass _Entity [] [])


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


(defn Polygon [n]
  (setv p (_Entity))

  (setv p.fill [1 1 1 1])
  (setv p.stroke [1 1 1 1])

  ; vertex_list has to be generated inside draw
  (setv p.wired-list None)
  (setv p.solid-list None)

  (defn draw []
    (unless p.wired-list
      (setv p.wired-list
            (build-wired-list n)))

    (unless p.solid-list
      (setv p.solid-list
            (build-solid-list n)))

    (setv p.wired-list.colors
          (* (color p.stroke) n))

    (setv p.solid-list.colors
          (* (color p.fill) (* n 3)))

    (.draw p.solid-list gl.GL_TRIANGLES)
    (.draw p.wired-list gl.GL_LINE_LOOP))

  (setv p.draw draw)
  p)


(defn blit-img [img]
  (.blit img
         -1 1 0
         2 -2))


(defn new-blittable [inner]
  (setv entity (_Entity))

  (defn blit []
      (blit-img inner))

  (setv entity.blit blit)
  entity)


(defn Frame []
  (setv frame (_Entity))

  (defn blit []
    (setv texture (_getRenderTexture))
    (when texture
      (blit-img texture)))

  (setv frame.blit blit)
  frame)


(defn Image [name]
  "
  Image from png file
  "
  (new-blittable (apply pyglet.image.load
                        [(+ "images/" name ".png")]
                        {"decoder" (PNGImageDecoder)})))

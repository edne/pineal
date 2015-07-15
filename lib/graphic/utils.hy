(import
  [pyglet.gl :as gl]
  [pyglet.graphics [vertex_list]]
  [pyglet.image]
  [pyglet.image.codecs.png [PNGImageDecoder]]
  [lib.windows [getRenderTexture :as _getRenderTexture]]
  [math [cos sin pi]]
  [time [time]]
  [lib.graphic.transforming [*]]
  [lib.graphic.framebuffer [Framebuffer]]
  [lib.graphic.coloring [*]])

(require hy.contrib.multi)


(defn time2rad [&optional [mult 1]]
  "trigonometric functions don't handle really high numbers"
  (% (* mult (time)) (* 2 pi)))


(defn nestle [&rest fs]
  (defn nestle-inner [&rest fs]
    (if (cdr fs)
      ((car fs) (apply nestle-inner (cdr fs)))
      (car fs)))
  (apply nestle-inner fs))


(defn pack [f]
  (fn [&optional next]
      (if next
      (fn []
          (f)
          (next))
      (f))))


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


(def memo-solid {})

(defn psolid [n]
  (defn fill [fill-color]
    (pack
        (fn []
            (unless (in n memo-solid)
              (assoc memo-solid n
                     (build-solid-list n)))

            (setv solid-list
                  (get memo-solid n))
            (setv solid-list.colors
                  (* (color fill-color) (* n 3)))

            (.draw solid-list gl.GL_TRIANGLES)))))


(def memo-wired {})

(defn pwired [n]
  (defn stroke [stroke-color]
    (pack
        (fn []
            (unless (in n memo-wired)
              (assoc memo-wired n
                     (build-wired-list n)))

            (setv wired-list
                  (get memo-wired n))
            (setv wired-list.colors
                  (* (color stroke-color) n))

            (.draw wired-list gl.GL_LINE_LOOP)))))


(defn blit-img [img]
  (.blit img
         -1 1 0
         2 -2))


(defn new-blittable [inner]
  (fn []
      (blit-img inner)))


(def frame
     (pack (fn []
               (setv texture (_getRenderTexture))
               (when texture (blit-img texture)))))


(def memo-img {})

(defn image [name]
  "
  Image from png file
  "
  (pack
      (fn []
          (unless (in name memo-img)
            (assoc memo-img name
                   (new-blittable (apply pyglet.image.load
                                         [(+ "images/" name ".png")]
                                         {"decoder" (PNGImageDecoder)}))))
          ((get memo-img name)))))


(def memo-buffer {})

(defn frame-buffer [name]
  "
  Magic cloak over FrameBuffer
  "
  (defclass buffer-class [Framebuffer]
    [[--call--
      (fn [self &optional next]
        (setv f (fn []
                  (blit-img self.texture)))
        (if next
          (fn []
            (f)
            (next))
          (f)))]])

  (unless (in name memo-buffer)
    (assoc memo-buffer name
      (buffer-class 800 800)))

  (get memo-buffer name))

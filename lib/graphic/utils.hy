(import
  [pyglet.gl :as gl]
  [pyglet.image]
  [pyglet.image.codecs.png [PNGImageDecoder]]
  [math [pi]]
  [time [time]]
  [lib.graphic.transforming [*]]
  [lib.graphic.framebuffer [Framebuffer]]
  [core.shapes [solid-polygon
                wired-polygon]]
  [tools.coloring [*]])


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


(def memo-solid {})

(defn psolid [n]
  (defn fill [fill-color]
    (pack
        (fn []
            (unless (in n memo-solid)
              (assoc memo-solid n
                     (solid-polygon n)))

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
                     (wired-polygon n)))

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

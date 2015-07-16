(import
  [pyglet.gl :as gl]
  [pyglet.image]
  [pyglet.image.codecs.png [PNGImageDecoder]]
  [lib.graphic.transforming [*]]
  [lib.graphic.framebuffer [Framebuffer]]
  [core.shapes [solid-polygon
                wired-polygon]]
  [tools.coloring [*]])


(defn nestle [&rest fs]
  (defn nestle-inner [&rest fs]
    (if (cdr fs)
      ((car fs) (apply nestle-inner (cdr fs)))
      (car fs)))
  (apply nestle-inner fs))


(defn pack [f &rest args &kwargs kwargs]
  (fn [&optional next]
      (if next
      (fn []
          (apply f args kwargs)
          (next))
      (apply f args kwargs))))


(defclass Entity []
  [[setup (fn [self])]
   [draw (fn [self])]

   [--init--
    (fn [self
         &rest args
         &kwargs kwargs]
      (apply self.setup args kwargs)
      None)]

   [--call--
    (fn [self
         &rest args
         &kwargs kwargs]

      (apply pack
        (+ [self.draw]
           (list args))
        kwargs))]])


(defclass psolid [Entity]
  [[memo {}]

   [setup
    (fn [self n]
      (setv self.n n))]

   [draw
    (fn [self solid-color]
      (setv n self.n)
      (unless (in n self.memo)
        (assoc self.memo n
          (solid-polygon n)))

      (setv solid-list
        (get self.memo n))
      (setv solid-list.colors
        (* (color solid-color) (* n 3)))

      (.draw solid-list gl.GL_TRIANGLES))]])


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

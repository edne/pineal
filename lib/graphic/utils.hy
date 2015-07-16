(import
  [pyglet.image]
  [pyglet.image.codecs.png [PNGImageDecoder]]
  [lib.graphic.transforming [*]]
  [lib.graphic.framebuffer [Framebuffer]])


(defn nestle [&rest fs]
  (defn nestle-inner [&rest fs]
    (if (cdr fs)
      ((car fs) (apply nestle-inner (cdr fs)))
      (car fs)))
  (apply nestle-inner fs))


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
  (_pack
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

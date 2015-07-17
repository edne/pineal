(import
  [lib.graphic.framebuffer [Framebuffer]])


(defn nestle [&rest fs]
  (defn nestle-inner [&rest fs]
    (if (cdr fs)
      ((car fs) (apply nestle-inner (cdr fs)))
      (car fs)))
  (apply nestle-inner fs))


(def memo-buffer {})

(defn frame-buffer [name]
  "
  Magic cloak over FrameBuffer
  "
  (defclass buffer-class [Framebuffer]
    [[--call--
      (fn [self &optional next]
        (setv f (fn []
      (.blit self.texture
             -1 1 0
             2 -2)))
        (if next
          (fn []
            (f)
            (next))
          (f)))]])

  (unless (in name memo-buffer)
    (assoc memo-buffer name
      (buffer-class 800 800)))

  (get memo-buffer name))

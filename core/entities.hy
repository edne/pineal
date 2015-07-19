(import [core.framebuffer [Framebuffer]])

(defclass BaseEntity []
  [[--init--
    (fn [self
         &rest args
         &kwargs kwargs]
      (setv self._args args)
      (setv self._kwargs kwargs)
      None)]])


(defclass Entity [BaseEntity]
  [[draw (fn [self])]

   [--call--
    (fn [self &optional f]
      (if f
        (fn []
          (apply self.draw self._args self._kwargs)
          (f))
        (apply self.draw self._args self._kwargs)))]])


(defclass Effect [BaseEntity]
  [[wrap
    (fn [self f]
      (f))]

   [--call--
    (fn [self &optional f]
      (when f
        (fn []
          (apply self.wrap
            (+ [f] (list self._args))
            self._kwargs))))]])


(defclass Layer [BaseEntity]
  [[memo {}]

   [draw
    (fn [self]
      (.blit self.buffer.texture
             -1 1 0
             2 -2))]

   [--init--
    (fn [self name]
      (.--init-- BaseEntity self)
      (unless (in name self.memo)
        (assoc self.memo name
          (Framebuffer 800 800)))

      (setv self.buffer (get self.memo name))
      None)]

   [--call--
    (fn [self &optional f]
      (if f
        (fn []
          (self.draw)
          (f))
        (self.draw)))]

   [--enter--
    (fn [self]
      (self.buffer.--enter--))]

   [--exit--
    (fn [self
         &rest args
         &kwargs kwargs]
      (apply self.buffer.--exit-- args kwargs))]])

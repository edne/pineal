(import [core.framebuffer [Framebuffer]])


(defclass Entity []
  [[draw
    (fn [self
         &rest args
         &kwargs kwargs])]

   [wrap
    (fn [self fs
         &rest args
         &kwargs kwargs]
      (for [f fs]
        (f)))]

   [--init--
    (fn [self
         &rest args
         &kwargs kwargs]
      (setv self._args args)
      (setv self._kwargs kwargs)
      None)]

   [--call--
    (fn [self &rest fs]
      (if fs
        (LambdaEntity (fn []
                        (apply self.draw self._args self._kwargs)
                        (apply self.wrap
                          (+ [fs] (list self._args))
                          self._kwargs)))
        (apply self.draw self._args self._kwargs)))]

   [--or--
    (fn [self other]
      (other self))]])


(defclass LambdaEntity [Entity]
  [[--init--
    (fn [self f]
      (.--init-- Entity self)
      (setv self.draw f)
      None)]])


(defclass Effect [Entity] [])


(defclass Layer [Entity]
  [[memo {}]

   [draw
    (fn [self]
      (.blit self.buffer.texture
             -1 1 0
             2 -2))]

   [--init--
    (fn [self name]
      (.--init-- Entity self)
      (unless (in name self.memo)
        (assoc self.memo name
          (Framebuffer 800 800)))

      (setv self.buffer (get self.memo name))
      None)]

   [--enter--
    (fn [self]
      (self.buffer.--enter--))]

   [--exit--
    (fn [self
         &rest args
         &kwargs kwargs]
      (apply self.buffer.--exit-- args kwargs))]])

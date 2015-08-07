(import
  [core.framebuffer [Framebuffer]])


(defclass BaseEntity []
  [[--init--
    (fn [self
         &rest args
         &kwargs kwargs]
      ; entities like Psolid take arguments in the
      ; constructor, and process them in draw() 
      (setv self._args (list args))
      (setv self._kwargs kwargs)
      None)]])


(defclass Entity [BaseEntity]
  [[draw
    (fn [self
         &rest args
         &kwargs kwargs])] 

   [--call--
    (fn [self]
      (apply self.draw self._args self._kwargs))]])


(defclass Effect [BaseEntity]
  [[wrap
    (fn [self fs
         &rest args
         &kwargs kwargs]
      (for [f fs]
        (f)))]

   [--call--
    (fn [self &rest fs]
      (if fs
        (fn []
          (apply self.wrap
            (+ [fs] self._args)
            self._kwargs))))]])


(defclass Layer [Entity Effect]
  [[memo {}]

   [draw
    (fn [self]
      (.blit self.buffer.texture
             -1 1 0
             2 -2))]

   [wrap
    (fn [self fs]
      (self.buffer.--enter--)
      (for [f fs]
        (f))
      (self.buffer.--exit--))]

   [--init--
    (fn [self name]
      (unless (in name self.memo)
        (import [core [conf]])
        (assoc self.memo name
          (apply Framebuffer conf.RENDER-SIZE)))

      (.--init-- Entity self)
      (.--init-- Effect self)

      (setv self.buffer (get self.memo name))
      None)]

   [--call--
    (fn [self &rest fs]
      (if fs
        (fn [] (.wrap self fs))
        (.--call-- Entity self)))]

   [--enter--
    (fn [self]
      (self.buffer.--enter--))]

   [--exit--
    (fn [self
         &rest args
         &kwargs kwargs]
      (apply self.buffer.--exit-- [] {}))]])

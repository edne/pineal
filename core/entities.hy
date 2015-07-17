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

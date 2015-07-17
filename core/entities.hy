(defclass Entity []
  [[draw (fn [self])]

   [--init--
    (fn [self
         &rest args
         &kwargs kwargs]
      (setv self._args args)
      (setv self._kwargs kwargs)
      None)]

   [--call--
    (fn [self &optional f]
      (if f
        (fn []
          (apply self.draw self._args self._kwargs)
          (f))
        (apply self.draw self._args self._kwargs)))]])

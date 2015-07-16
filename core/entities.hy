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

      (fn [&optional f]
        (if f
          (fn []
            (apply self.draw args kwargs)
            (f))
          (apply self.draw args kwargs))))]])

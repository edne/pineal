(defn _pack [f &rest args &kwargs kwargs]
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

      (apply _pack
        (+ [self.draw]
           (list args))
        kwargs))]]) 

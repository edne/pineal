(defn nestle [&rest fs]
  (defn nestle-inner [&rest fs]
    (if (cdr fs)
      ((car fs) (apply nestle-inner (cdr fs)))
      (car fs)))
  (apply nestle-inner fs))

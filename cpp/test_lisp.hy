(require pineal.dsl)
(import [math [pi]])

(loop
  (window asd
          (polygon 4
                   ["fill" 0 1 1 1]
                   ["rotate" (/ pi 4)]
                   ["translate" 0.5 0]
                   ["scale" 0.2])))

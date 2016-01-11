(require pineal.dsl)
(import [math [pi]])

(loop
  (window asd
          (group
            [(polygon 4
                      ["fill" (color 0 1 1)]
                      ["rotate" (/ pi 4)]
                      ["translate" 0.5 0]
                      ["scale" 0.5])

             (polygon 8
                      ["scale" 0.2]
                      ["stroke" (color 0 0 1)])]

            ["line" 0.05]
            ["fill" (color 0.5)]
            ["stroke" (color 0 1 0)])))

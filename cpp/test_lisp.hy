(require pineal.dsl)
(import [math [pi]])



(loop
  (layer "render"
         (transform
           [(group
              [(polygon 4
                        ["fill" (color 0 1 1)]
                        ["rotation" (/ pi 4)]
                        ["position" 0.5 0]
                        ["radius" 0.5])

               (polygon 8
                        ["radius" 0.2]
                        ["stroke" (color 0 0 1)])]

              ["line" 0.05]
              ["fill" (color 0.5)]
              ["stroke" (color 0 1 0)])

            (polygon 3
                     ["radius" 0.1]
                     ["position" 0 0.1]) ]

           ["rotate" (/ pi 6)]))

  (window "master"
          (layer "render"))

  (window "overwiew"
          (layer "render")))

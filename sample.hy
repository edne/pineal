(import [tools [*]])

(def amp  (osc-in "/amp"))
(def bass (osc-in "/bass"))
(def high (osc-in "/high"))

(def grey (palette "kw"))
(def hsv (palette "rgbr"))


(defn draw []
  (stroke-weight 4)

  (on-layer "master"
            (group
              [(apply-effects
                 (psolid 4 (grey 0 0.01))
                 [(scale 4)])

               (apply-effects
                 (group
                   [(pwired 3 (hsv (amp 4)))
                    (apply-effects
                      (fn [] (draw-layer "master"))
                      [(scale (bass 1 0.8))
                       (rotate (/ pi 4))])])

                 [(scale (bass 8 0.8))
                  (rotate (/ pi 6))])

               (apply-effects
                 (psolid 4 (grey 1))
                 [(scale 0.5)
                  (rotate (/ pi 4))])]))

  (draw-layer "master"))

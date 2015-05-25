(import
  [osc [nerve-send nerve-cb!]])


(defn source [code]
  "Permits to get audio signals in the livecoding part"

  (setv container [0])

  (nerve-send "/ear/code" [code])

  (nerve-cb! (+ "/eye/audio/" code)
             (fn [path args]
                 (setv [(car container)] args)))

  (fn [] (car container)))

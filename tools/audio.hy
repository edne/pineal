(import
  [core.nerve [nerve-cb!]])


(defn new-source [name]
  (setv container [0])

  (nerve-cb! name
             (fn [path args]
               (setv [(car container)] args)))

  (fn [] (car container)))


(def amp (new-source "/eye/audio/amp"))

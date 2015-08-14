(import [core.nerve [nerve-cb!]])


(def memo-source {})

(defn get-source [name]
  (unless (in name memo-source)
    (setv container [0])

    (nerve-cb! name
               (fn [path args]
                 (setv [(car container)] args)))

    (assoc memo-source
      name (fn [] (car container))))

  (get memo-source name))

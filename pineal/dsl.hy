(defmacro draw [&rest body]
  `(do
     (import pineal)
     (import [pineal.graphic [*]])
     (import [time [time]])
     (import [math [*]])

     (when (= __name__ "__main__")
       (pineal.run __file__))

     (def false False)
     (def true True)

     (defn on-layer [name &rest items]
       (for [item items]
         (-> item (.on-layer name) (.draw))))

     (defn on-window [name show-fps &rest items]
       (for [item items]
         (-> item (.window name show-fps) (.draw))))

     (defn draw []
       ~@body)))

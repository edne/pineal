(require pineal.core)


(defn test-vision []
  (import [pineal.eye [new-vision]])
  (setv vision (new-vision "tested-vision" "failing code"))
  (assert (= (vision) :broken))
  (assert (= (vision) :working))
  (assert (= (vision) :working)))


(defn test-eval-str []
  (import [pineal.eye [eval-str]])
  (assert (= (eval-str "1" {}) 1))
  (assert (= (eval-str "(+ 1 2)" {}) 3))
  (assert (= (eval-str "(setv x 1) (+ x 1)" {}) 2)))


(defn test-main []
  (start-pineal)
  (stop-pineal))

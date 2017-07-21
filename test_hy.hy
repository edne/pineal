#!/usr/bin/env hy
(import pineal)
(import [pineal.graphic [polygon]])

(when (= __name__ "__main__")
  (pineal.run __file__))


(defn draw []
  (-> (polygon 4 [1])
    (.window "master")
    (.draw)))

#!/usr/bin/env hy
(require [pineal.dsl [draw]])

(draw
  (stroke-weight 1)
  (on-layer "lv1"
             (-> (polygon 4 [0 0.1])
               (.scale 4))

             (-> (layer "lv1")
               (.scale 1.5))

             (-> (polygon 4 [1] false)
               (.scale 0.5)
               ;(.scale (-> (time) (% (* 2 pi)) sin))
               (.rotate (-> (time) (* 0.2) (% (* 2 pi))) [0 1 0])
               (.rotate (-> (time) (* 1.3) (% (* 2 pi))) [1 0 0]))

             (-> (layer "lv1")
               (.scale 0.1)))

  (on-window "master" false
             (layer "lv1")))

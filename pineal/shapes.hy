(import
  [math [sin cos pi]]
  [pyglet.graphics [vertex-list]])


(defn wired-polygon [n]
  (vertex-list n
               (tuple ["v2f/static"
                       (flatten
                         (map (fn [i]
                                (setv theta
                                  (-> (/ pi n)
                                    (* 2 i)))
                                [(cos theta) (sin theta)])
                           (range n)))])
               (tuple ["c4f/stream"
                       (* [1] 4 n)])))


(defn solid-polygon [n]
  (vertex-list (* n 3)
               (tuple ["v2f/static"
                       (flatten
                         (map (fn [i]
                                (setv dtheta
                                  (* 2 (/ pi n)))
                                (setv theta0
                                  (* i dtheta))
                                (setv theta1
                                  (+ theta0 dtheta))
                                [ 0 0
                                 (cos theta0) (sin theta0)
                                 (cos theta1) (sin theta1)])
                           (range n)))])
               (tuple ["c4f/stream"
                       (* [1] 4
                         (* n 3))])))

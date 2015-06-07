(import
  [pyglet.gl :as gl]
  [math [pi]])

(require hy.contrib.multi)


(def _matrix_sp 0)


(defn push []
  (global _matrix_sp)
  (if (< _matrix_sp 30)
    (do
      (gl.glPushMatrix)
      (+= _matrix_sp 1)
      true)
    false))


(defn pop []
  (global _matrix_sp)
  (if (> _matrix_sp 0)
    (do
      (gl.glPopMatrix)
      (-= _matrix_sp 1)
      true)
    false))


(defn _transform [ transformation
                   &rest tr-args
                   &kwargs tr-kwargs]
  (fn [f]
      (fn [&rest args &kwargs kwargs]
          (push)
          (apply transformation
                 tr-args tr-kwargs)
          (apply f args kwargs)
          (pop))))


(defmulti scale
          ([s]     (scale s s s))
          ([x y]   (scale x y 1))
          ([x y z] (_transform gl.glScalef
                               x y z)))


(defmulti rotate
          ([angle] (rotate angle 0 0 1))
          ([angle x y z]
           (_transform gl.glRotatef
                       (/ (* angle 180) pi)
                       x y z)))


(defmulti translate
          ([x]     (translate x 0 0))
          ([x y]   (translate x y 0))
          ([x y z] (_transform gl.glTranslatef
                               x y z)))


(defn turnaround [n]
  "Decorator to rotate N times"
  (defn decorator [f]
    (defn decorated [&rest args &kwargs kwargs]
      (for [i (range n)]
           (push)
           (setv angle (/ (* 2 pi i) n))
           (gl.glRotatef (/ (* angle 180) pi)
                         0 0 1)
           (apply f args kwargs)
           (pop)))))

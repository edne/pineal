(import [pyglet.gl :as gl]
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

(defn pushmatrix [f]
  "
  Decorator to handle matrix stack
  that can be used as implicit exit condition in recursions
  "
  (defn decorated [&rest args &kwargs kwargs]
    (if (push)
      (do
        (apply f args kwargs)
        (pop)))))


(defmulti scale
  ([s] (gl.glScalef s s s))
  ([x y] (gl.glScalef x y 1))
  ([x y z] (gl.glScalef x y z)))


(defmulti rotate
  ([angle]
    (gl.glRotatef (/ (* angle 180) pi) 0 0 1))
  ([angle x y z]
    (gl.glRotatef (/ (* angle 180) pi) x y z)))

(defn rotateX [angle]
  (gl.glRotatef
      (* pi (/ angle 180))
      1 0 0))

(defn rotateY [angle]
  (gl.glRotatef
      (/ (* angle 180) pi)
      0 1 0))

(defn rotateZ [angle]
  (gl.glRotatef
      (/ (* angle 180) pi)
      0 0 1))


(defmulti translate
  ([x] (gl.glTranslatef x 0 0))
  ([x y] (gl.glTranslatef x y 0))
  ([x y z] (gl.glTranslatef x y z)))


(defn turnaroud [n &optional [r 0]]
  "Decorator to rotate N times"
  (defn decorator [f]
    (defn decorated [&rest args &kwargs kwargs]
      (for [i (range n)]
        (push)
        (rotate (/ (* 2 pi i) n))
        (translate r)
        (apply f args kwargs)
        (pop))
      )))

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
    (gl.glLoadIdentity))))

(defn pop []
  (global _matrix_sp)
  (if (> _matrix_sp 0)
    (do
      (gl.glPopMatrix)
      (-= _matrix_sp 1))
    (gl.glLoadIdentity)))


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
  ([x y] (gl.glTranslatef x y 0))
  ([x y z] (gl.glTranslatef x y z)))



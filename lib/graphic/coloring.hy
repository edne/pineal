(import [pyglet.gl :as gl]
        [colorsys [hsv_to_rgb]])

(require hy.contrib.multi)


(defmulti _color
  ([x]       [x x x 1])
  ([x a]     [x x x a])
  ([r g b]   [r g b 1])
  ([r g b a] [r g b a]))
(defn color [c]
  (apply _color (flatten [c])))


(defun rgb [&rest args]
  (color args))

(defmulti hsv
  ([h]       (hsv_to_rgb h 1 1))
  ([h s v]   (hsv_to_rgb h s v))
  ([h s v a] (+ (list (hsv_to_rgb h s v)) [a]))
  ([h a] (hsv h 1 1 a)))


(defn strokeWeight [weight]
  (gl.glLineWidth weight))

(require pineal.macros)

(defmacro stop-eye   []
  '(when (in "eye"   (vars)) (.stop eye)))

(defmacro stop-ear   []
  '(when (in "ear"   (vars)) (.stop ear)))

(defmacro stop-coder []
  '(when (in "coder" (vars)) (.stop coder)))


(defmacro start-eye []
  '(do
     (import [pineal.eye [eye-runner]])
     (stop-eye)
     (setv eye (eye-runner))
     (.start eye)))

(defmacro start-ear []
  '(do
     (import [pineal.ear [ear-runner]])
     (stop-ear)
     (setv ear (ear-runner))
     (.start ear)))

(defmacro start-coder []
  '(do
     (import [pineal.coder [coder-runner]])
     (stop-coder)
     (setv coder (coder-runner))
     (.start coder))) 

(defmacro start-pineal []
  '(do
     (start-eye)
     (start-ear)
     (start-coder)))

(defmacro stop-pineal []
  '(do
     (stop-eye)
     (stop-ear)
     (stop-coder)))

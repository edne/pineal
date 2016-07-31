(defmacro --header-- []
  "Things to do outside the --draw-- function"
  '(do
     (import
       [math [*]]
       [core [*]])

     (def 2pi (* 2 pi))
     (def time (osc_value (str "/time")))
     (def amp (osc_value (str "/amp")))
     ))

; To use this file as imported module
(--header--)


(defn draw [entity]
  (entity))


(defmacro bind-action [action]
  `(defn ~action [&rest args]
     (make-action (str '~action) (list args))))

(bind-action compose)
(bind-action branch)
(bind-action hide)
(bind-action scale)
(bind-action translate)
(bind-action rotate-x)
(bind-action rotate-y)
(bind-action rotate-z)
(bind-action color)
(bind-action fill)
(bind-action no-fill)
(bind-action line-width)


(defn change [entity &rest actions]
  (make-entity (str "change")
               [entity (apply compose actions)]))

(defn group [&rest entities]
  (make-entity (str "group")
               (list entities)))

(defn cube    []       (make-entity (str "cube")    []))
(defn polygon [n]      (make-entity (str "polygon") [n]))
(defn text    [font s] (make-entity (str "text")    [(str font) (str s)]))

(defn rgb    [&rest args] (make-color (str "rgb")    (list args)))
(defn lerp   [&rest args] (make-color (str "lerp")   (list args)))
(defn invert [&rest args] (make-color (str "invert") (list args)))


(defmacro group-for [item-iterator &rest entities]
  (setv [item iterator] item-iterator)
  `(apply group (map (fn [~item]
                       (group ~@entities))
                  ~iterator)))

(defmacro branch-for [item-iterator &rest actions]
  (setv [item iterator] item-iterator)
  `(apply branch (map (fn [~item]
                        (compose ~@actions))
                   ~iterator)))


(defmacro get-osc-f [path]
  `(get-osc-f_c (str ~path)))


;(defmacro beat [n entity pos dur]
;  `(~entity (at-beat [~n ~pos ~dur])))


;(defmacro seq [n &rest args]
;  `(do
;     (setv clips [])

;     (for [[pos e dur] [~@args]]
;       (setv a (at-beat [~n pos dur]))
;       (.append clips (change e a)))

;     (group_c clips)))


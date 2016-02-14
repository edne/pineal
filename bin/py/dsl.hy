(defmacro --header-- []
  "Things to do outside the --draw-- function"
  '(do
     (import [core [*]])
     (import [math [*]])
     (import [time [time]])))


(defmacro alias [name &rest body]
  "Define simple macros to replace name and first parameters"
  `(defmacro ~name [&rest args]
     `(~@'~body ~@args)))


(defmacro -@> [head &rest tail]
  "Threading wrapping macro, like `->` but wraps the head with a lambda"
  (if-not tail 
    head
    (let [[next (first tail)]]
      `(-@> (~(first next) (fn [] ~head)
                           ~@(rest next))
            ~@(rest tail)))))

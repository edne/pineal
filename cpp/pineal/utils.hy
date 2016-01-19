(import
  [hy.lex [tokenize]]
  [hy.importer [hy-eval]])

(defn hy_eval_string [s namespace]
  "Eval Hy code from string"
  (hy-eval `(do ~@(tokenize s))
           namespace --name--))

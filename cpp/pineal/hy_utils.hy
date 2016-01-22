(import
  [hy.lex [tokenize]]
  [hy.importer [hy-eval]])

(defn eval_hy_code [s namespace]
  "Eval Hy code from string"
  (hy-eval `(do ~@(tokenize s))
           namespace --name--))

(defn new-logger [name conf]
  (import [logging])

  (setv numeric-level (getattr logging
                               (.upper conf.LOG-LEVEL)
                               None))

  (unless (isinstance numeric-level
                      int)
    (raise (ValueError "Invalid log level")))

  (apply logging.basicConfig
    [] {"level" numeric-level})

  (setv logger (logging.getLogger name))
  logger)

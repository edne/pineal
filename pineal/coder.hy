(import
  [glob [glob]]
  [os.path [abspath]]
  [os.path [split :as path-split]]
  [time [sleep]]
  [watchdog.observers [Observer]]
  [watchdog.events [FileSystemEventHandler]]
  [liblo])

(require pineal.macros)


(runner coder-runner [conf log]
        "
        Wait for changes
        "
        (log.info "starting coder.hy")

        (defn new-handler [file-name]
          (defn get-code []
            (with [[f (open file-name)]]
              (.read f)))

          (defn valid? [path]
            (= (abspath path)
              (abspath file-name)))

          (liblo.send conf.OSC_EYE
                      "/eye/code" (, (str "s") (get-code)))

          (defclass Handler [FileSystemEventHandler]
            [[on-modified
               (fn [self event]
                 (when (valid? event.src-path)
                   (liblo.send conf.OSC_EYE
                               "/eye/code" (, (str "s") (get-code)))))]])
          (Handler))

        (let [[observer (Observer)]
              [file-name conf.file-name]]
          (.schedule observer
                     (new-handler file-name)
                     (-> file-name
                       abspath path-split first) false)
          (.start observer)

          (running (sleep (/ 1 60)))
          (log.info "stopping coder.hy")

          (.stop observer)
          (.join observer)))

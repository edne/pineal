(import
  [glob [glob]]
  [os.path [abspath]]
  [os.path [split :as path-split]]
  [time [sleep]]
  [watchdog.observers [Observer]]
  [watchdog.events [FileSystemEventHandler]]
  [pineal.osc [osc-sender]])

(require pineal.macros)


(runner coder-runner [conf log]
        "
        Wait for changes
        "
        (log.info "starting coder.hy")

        (let [[observer (Observer)]
              [file-name conf.file-name]]
          (.schedule observer
                     (new-handler file-name
                                  (osc-sender conf.OSC_EYE))
                     (-> file-name
                       abspath path-split first) false)
          (.start observer)

          (running (sleep (/ 1 60)))
          (log.info "stopping coder.hy")

          (.stop observer)
          (.join observer)))


(defn new-handler [file-name osc-send]
  (defn get-code []
    (with [[f (open file-name)]]
      (.read f)))

  (defn valid? [path]
    (= (abspath path)
      (abspath file-name)))

  (osc-send "/eye/code"
            [file-name (get-code)])

  (defclass Handler [FileSystemEventHandler]
    [[on-modified
       (fn [self event]
         (when (valid? event.src-path)
           (osc-send "/eye/code"
                     [file-name (get-code)])))]])
  (Handler))

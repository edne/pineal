#!/usr/bin/env hy

(import
  [sys [exit]]
  [time [sleep]]
  [hy.lex [tokenize]]
  [pyo]
  [core.osc [osc-sender]])


(require core.macros)


(runner Ear [conf log]
        (log.info "starting ear.hy")

        (setv pyo-server
          (apply pyo.Server
            []
            {"audio" conf.BACKEND
             "jackname" "(pineal)"
             "nchnls" 2}))

        (if (= conf.BACKEND "jack")
          (.setInputOffset pyo-server 2))

        (.boot pyo-server)
        (.start pyo-server)

        (try (do
               (setv src
                 (apply pyo.Input
                   []
                   {"chnl" [0 1]}))
               (log.info "Pyo is working properly!\n"))
          (catch [pyo.PyoServerStateException]
            (log.error "Pyo is not working")
            (exit 1)))

        (setv _osc-send (osc-sender conf.OSC_EYE))
        (setv osc-send
          (fn [path val]
            (log.debug (+ path " " (str val)))
            (_osc-send path val)))

        (setv amp  (pyo.Follower src))

        (running (osc-send "/eye/audio/amp"
                           (float (.get amp)))

                 (sleep (/ 1 30)))

        (log.info "stopping ear.hy")
        (.stop pyo-server)
        (del pyo-server))


(defmain [args]
  (.run (Ear)))

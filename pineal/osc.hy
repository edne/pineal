(import
  [time [sleep]]
  [thirdparty.OSC [OSCServer
                   OSCClient
                   OSCClientError
                   OSCMessage]])

(require pineal.macros)


(defn osc-receiver [in_addr cbs]

  (defn callback [path tags args source]
    (for [k (.keys cbs)]
      (if (.startswith path k)
        ((get cbs k) path args))))

  (setv server
    (-> in_addr tuple OSCServer))

  (.addMsgHandler server
                  "default"
                  callback)

  (runner Receiver [conf log]
          (running
            (.handle_request server))
          (.close server))

  (setv receiver (Receiver))

  (defn start []
    (.start receiver)
    (fn [] (.stop receiver)))

  start)


(defn osc-sender [out_addr]
  (setv client (OSCClient))

  (.connect client
            (tuple out_addr))

  (fn [path args]
    (try (.send client
                (OSCMessage path args))
      (catch [OSCClientError] None))))

(import [lib.runner [Runner]])
(import [thirdparty.OSC [OSCServer OSCClient OSCClientError OSCMessage]])

(defclass Osc [Runner]
  [ [__init__ (fn [self]
      (.__init__ Runner self)
      (def self.server None)
      (def self.client {})
      (def self.cbs {})
      None)]

    [reciver (fn [self in_addr]
      (def self.server (-> in_addr tuple OSCServer))
      (.addMsgHandler self.server "default" self.callback))]

    [sender (fn [self out_addr]
      (def (get self.client out_addr) (OSCClient))
      (.connect (get self.client out_addr) (tuple out_addr)))]

    [run (fn [self]
      (.iteration self (fn []
        (.handle_request self.server)))
      (.close self.server))]

    [listen (fn [self key cb]
      (def (get self.cbs key) cb))]

    [callback (fn [self path tags args source]
      (for [k (.keys self.cbs)]
        (if (.startswith path k)
          ((get self.cbs k) path args))))]

    [send (fn [self path args &optional [out_addr None]]
      (try
        (if self.client
          (.send
            (if out_addr
              (get self.client out_addr)
              (get self.client (first self.client)))
            (OSCMessage path args)))
      (catch [OSCClientError] None)))]])

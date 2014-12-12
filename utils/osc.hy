(import [runner [Runner]])
(import [thirdparty.OSC [OSCServer OSCClient OSCClientError OSCMessage]])

(defclass Osc [Runner]
  [ [__init__ (fn [self]
      (.__init__ Runner self)
      (def self.server None)
      (def self.client None)
      (def self.cbs {})
      None)]

    [reciver (fn [self in_addr]
      (def self.server (-> in_addr tuple OSCServer))
      (.addMsgHandler self.server "default" self.callback))]

    [sender (fn [self out_addr]
      (def self.client (OSCClient))
      (.connect self.client (tuple out_addr)))]

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

    [send (fn [self path args]
      (try
        (if self.client
          (.send self.client (OSCMessage path args)))
      (catch [OSCClientError] None)))]])

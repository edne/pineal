(import [lib.runner [Runner]]
        [time [sleep]]
        [thirdparty.OSC [OSCServer OSCClient OSCClientError OSCMessage]])


(defclass Osc [Runner]
  "
  Personal-use wrapper around thirdparty.OSC
  "
  [ [__init__ (fn [self]
      (.__init__ Runner self)
      (setv self.server None)
      (setv self.client {})
      (setv self.cbs {})
      None)]

    [receiver (fn [self in_addr]
      (setv self.server (-> in_addr tuple OSCServer))
      (.addMsgHandler self.server "default" self.callback))]

    [sender (fn [self out_addr]
      (assoc self.client out_addr (OSCClient))
      (.connect (get self.client out_addr) (tuple out_addr)))]

    [run (fn [self]
      (.while-not-stopped self (fn []
        (.handle_request self.server)))
      (.close self.server))]

    [listen (fn [self key cb]
      (assoc self.cbs key cb))]

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


; Osc instance used by Eye, it is here as singleton and not inside the Eye
; class in order to be accessible by audio.source and osc.source and permit
; to live-coded parts to exchange OSC signals with Universe
(def nerve (Osc))


(defn source [path]
  "A copy-paste from audio.source, should work but I've never tried"
  (defclass Status []
    [ [__init__ (fn [self]
        (setv self.v 0)
        None)]

      [cb (fn [self path args]
        (setv [self.v] args))]

      [getv (fn [self]
        self.v)]])

  (setv status (Status))

  (.listen nerve path status.cb)

  status.getv)

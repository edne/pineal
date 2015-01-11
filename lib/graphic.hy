(import [pyglet.gl :as gl]
        [math])

(defclass GLEntity []
  [ [vertsGl None]

    [_generateVerts
      (with-decorator staticmethod (fn []))]

    [__init__ (fn [self]
      (setv self.r 1)
      (setv [self.x self.y self.z] [0 0 0])
      (setv self.c [1 1 1 1])
      None)]

    [draw (fn [self])]])


(defclass PolInt [GLEntity]
  [ [_generateVerts
      (with-decorator staticmethod (fn [c n]
        (setv verts [])
        (setv theta 0)
        (for [i (range n)]
          (.append verts 0)
          (.append verts 0)

          (.append verts (math.cos theta))
          (.append verts (math.sin theta))

          (+= theta (/ (* 2 math.pi) n))

          (.append verts (math.cos theta))
          (.append verts (math.sin theta)))

        (setv c.vertsGl (apply (* gl.GLfloat (len verts)) verts))))]

    [draw (fn [self]
      (gl.glLoadIdentity)
      (gl.glTranslatef self.x self.y self.z)
      (gl.glScalef self.r self.r 1)

      (gl.glVertexPointer 2 gl.GL_FLOAT 0 self.vertsGl)

      (gl.glEnableClientState gl.GL_VERTEX_ARRAY)

      (apply gl.glColor4f self.c)
      (gl.glDrawArrays gl.GL_TRIANGLES 0 (len self.vertsGl))
      (gl.glTranslatef (- self.x) (- self.y) (- self.z)) )]])


(defn Polygon [n]
  (defclass PolClass [PolInt] [])
  (._generateVerts PolClass PolClass n)
  (PolClass))

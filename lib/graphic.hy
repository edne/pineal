(import [pyglet.gl :as gl]
        [math])

(defclass GLEntity []
  [ [vertsGl None]

    [_generateVerts
      (with-decorator staticmethod (fn []
        (setv verts [])
        (setv GLEntity.vertsGl
          (apply (* gl.GLfloat (len verts)) verts))))]

    [__init__ (fn [self]
      (setv self.r 1)
      (setv [self.x self.y self.z] [0 0 0])
      (setv self.fill [1 1 1 1])
      (setv self.stroke [1 1 1 1])
      None)]

    [draw (fn [self]
      (gl.glLoadIdentity)
      (gl.glTranslatef self.x self.y self.z)
      (gl.glScalef self.r self.r 1)

      (gl.glVertexPointer 2 gl.GL_FLOAT 0 self.vertsGl)

      (gl.glEnableClientState gl.GL_VERTEX_ARRAY)
      ;(gl.glPolygonMode gl.GL_FRONT gl.GL_LINE)

      (apply gl.glColor4f self.fill)
      (gl.glDrawArrays gl.GL_TRIANGLE_FAN 0 (len self.vertsGl))
      (apply gl.glColor4f self.stroke)
      (gl.glDrawArrays gl.GL_LINE_STRIP 0 (len self.vertsGl))
      (gl.glTranslatef (- self.x) (- self.y) (- self.z)) )]])


(defclass PolInt [GLEntity]
  [ [_generateVerts
      (with-decorator staticmethod (fn [c n]
        (setv verts [])

        (.append verts 0)
        (.append verts 0)

        (setv theta math.pi)
        (for [i (range (+ 1 n))]
          (.append verts (math.cos theta))
          (.append verts (math.sin theta))
          (+= theta (/ (* 2 math.pi) n))
          )

        (setv c.vertsGl
          (apply (* gl.GLfloat (len verts)) verts))))]])


(defn Polygon [n]
  (defclass PolClass [PolInt] [])
  (._generateVerts PolClass PolClass n)
  (PolClass))

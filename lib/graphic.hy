(import [pyglet.gl :as gl]
        [math])

(defclass GLEntity []
  [ [vertsGl None]

    [_generateVerts
      (with-decorator staticmethod (fn []
        (setv verts [])
        (setv GLEntity.vertsGl
          (apply (* gl.GLfloat (len verts)) verts))))]

    [__init__ (fn [self &optional [side 1]]
      (setv self.side side)
      None)]

    [draw (fn [self]
      (gl.glLoadIdentity)
      (gl.glScalef self.side self.side 1)
      (gl.glColor3f 1 1 1)

      (gl.glVertexPointer 2 gl.GL_FLOAT 0 self.vertsGl)

      (gl.glEnableClientState gl.GL_VERTEX_ARRAY)
      ;(gl.glPolygonMode gl.GL_FRONT gl.GL_LINE)
      (gl.glDrawArrays gl.GL_TRIANGLE_STRIP 0 (len self.vertsGl)))]])


(defclass PolInt [GLEntity]
  [ [_generateVerts
      (with-decorator staticmethod (fn [n]
        (setv verts [])
        (setv theta (/ math.pi -2))
        (for [i (range (+ 1 n))]
          (.append verts 0)
          (.append verts 0)

          (.append verts (math.cos theta))
          (.append verts (math.sin theta))

          (+= theta (/ (* 2 math.pi) n))

          (.append verts (math.cos theta))
          (.append verts (math.sin theta)))

        (setv PolInt.vertsGl
          (apply (* gl.GLfloat (len verts)) verts))))]])


(defn polygon [n]
  (defclass PolClass [PolInt] [])
  (._generateVerts PolClass n)
  (PolClass))

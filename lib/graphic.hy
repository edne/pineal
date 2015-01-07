(import [pyglet.gl :as gl]
        [math])

(defclass GLEntity []
  [ [vertsGl None]

    [_generateVerts
      (with-decorator staticmethod (fn []
        (setv verts [])
        (setv GLEntity.vertsGl
          (apply (* gl.GLfloat (len verts)) verts))))]

    [__init__ (fn [self &optional [r 1]]
      (setv self.r r)
      (setv self.fill [1 1 1])
      (setv self.stroke [1 1 1])
      None)]

    [draw (fn [self]
      (gl.glLoadIdentity)
      (gl.glScalef self.r self.r 1)

      (gl.glVertexPointer 2 gl.GL_FLOAT 0 self.vertsGl)

      (gl.glEnableClientState gl.GL_VERTEX_ARRAY)
      ;(gl.glPolygonMode gl.GL_FRONT gl.GL_LINE)

      (apply gl.glColor3f self.fill)
      (gl.glDrawArrays gl.GL_POLYGON 0 (len self.vertsGl))
      (apply gl.glColor3f self.stroke)
      (gl.glDrawArrays gl.GL_LINE_LOOP 0 (len self.vertsGl))
    )]])


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


(defn Polygon [n]
  (defclass PolClass [PolInt] [])
  (._generateVerts PolClass n)
  (PolClass))

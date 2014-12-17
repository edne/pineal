(import [pyglet.gl :as gl])

(defclass Entity []
  [ [vertsGl None]

    [_generateVerts
      (with-decorator staticmethod (fn []
        (setv verts [])
        (setv Entity.vertsGl
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
      (gl.glPolygonMode gl.GL_FRONT gl.GL_LINE)
      (gl.glDrawArrays gl.GL_QUADS 0 (len self.vertsGl))
      )]])


(defclass Square [Entity]
  [ [_generateVerts
      (with-decorator staticmethod (fn []
        (setv verts
          [-1 -1
            1 -1
            1  1
           -1  1])
        (setv Square.vertsGl
          (apply (* gl.GLfloat (len verts)) verts))))]])


(._generateVerts Entity)
(._generateVerts Square)

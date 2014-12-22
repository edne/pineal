(import [pyglet.gl :as gl])

(defclass GLEntity []
  [ [vertsGl None]

    [_generateVerts
      (with-decorator staticmethod (fn []
        (setv verts [])
        (setv GLEntity.vertsGl
          (apply (* gl.GLfloat (len verts)) verts))))]

    [__init__ (fn [self &optional [side 1]]
      (setv self.side (fn [] side))
      None)]

    [draw (fn [self]
      (gl.glLoadIdentity)
      (gl.glScalef (self.side) (self.side) 1)
      (gl.glColor3f 1 1 1)

      (gl.glVertexPointer 2 gl.GL_FLOAT 0 self.vertsGl)

      (gl.glEnableClientState gl.GL_VERTEX_ARRAY)
      ;(gl.glPolygonMode gl.GL_FRONT gl.GL_LINE)
      (gl.glDrawArrays gl.GL_QUADS 0 (len self.vertsGl))
      )]])


(defclass Square [GLEntity]
  [ [_generateVerts
      (with-decorator staticmethod (fn []
        (setv verts
          [-1 -1
            1 -1
            1  1
           -1  1])
        (setv Square.vertsGl
          (apply (* gl.GLfloat (len verts)) verts))))]])


(._generateVerts GLEntity)
(._generateVerts Square)

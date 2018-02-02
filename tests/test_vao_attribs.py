import struct
import unittest

import moderngl

from common import get_context


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = get_context()

    def test_vao_attribs(self):

        vertex_shader = self.ctx.vertex_shader('''
            #version 330

            in vec4 in_vert;
            out vec4 out_vert;

            void main() {
                out_vert = in_vert;
            }
        ''')

        program = self.ctx.program(vertex_shader, varyings=['out_vert'])

        vbo = self.ctx.buffer(struct.pack('12f', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
        res = self.ctx.buffer(reserve=struct.calcsize('8f'))

        vao = self.ctx.simple_vertex_array(program, vbo, 'in_vert')
        vao.transform(res, moderngl.POINTS, 2)

        for a, b in zip(struct.unpack('8f', res.read()), (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)):
            self.assertAlmostEqual(a, b)

        vao.bind('in_vert', vbo, offset=4, stride=0, divisor=0)
        vao.transform(res, moderngl.POINTS, 2)

        for a, b in zip(struct.unpack('8f', res.read()), (2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0)):
            self.assertAlmostEqual(a, b)

        vao.bind('in_vert', vbo, offset=8, stride=20, divisor=0)
        vao.transform(res, moderngl.POINTS, 2)

        for a, b in zip(struct.unpack('8f', res.read()), (3.0, 4.0, 5.0, 6.0, 8.0, 9.0, 10.0, 11.0)):
            self.assertAlmostEqual(a, b)

        vao.bind('in_vert', vbo, offset=12, stride=0, divisor=1)
        vao.transform(res, moderngl.POINTS, 2)

        for a, b in zip(struct.unpack('8f', res.read()), (4.0, 5.0, 6.0, 7.0, 4.0, 5.0, 6.0, 7.0)):
            self.assertAlmostEqual(a, b)

        with self.assertRaises(KeyError):
            vao.bind('in_vert_that_does_not_exist', vbo, offset=12, stride=0, divisor=1)


if __name__ == '__main__':
    unittest.main()

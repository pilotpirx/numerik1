top = '.'
out = 'build'

def options(opt):
    opt.load('compiler_c')

def configure(ctx):
    ctx.load('compiler_c python')
    ctx.env.append_unique('CFLAGS', ['-O3'])
    ctx.check_python_module('numpy')
    ctx.check_python_module('matplotlib')

def build(bld):
    bld.shlib(source='poly.c', target='poly')
    bld.program(source='aufgabe01.c poly.c', target='aufgabe01')

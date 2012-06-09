top = '.'
out = 'build'

def options(opt):
    opt.load('compiler_c')

def configure(ctx):
    ctx.load('compiler_c python')
    ctx.env.append_unique('CFLAGS', ['-O3', '-Wall'])
    ctx.check_python_module('numpy', mandatory=False)
    ctx.check_python_module('scipy', mandatory=False)
    ctx.check_python_module('matplotlib', mandatory=False)
    ctx.check_python_module('traits', mandatory=False)
    ctx.check_python_module('traitsui', mandatory=False)
    ctx.check_python_module('PyQt4', mandatory=False)
    ctx.check_cc(lib='gsl', uselib_store='gsl')
    ctx.check_cc(lib='gslcblas', uselib_store='cblas')
    ctx.check_cc(lib='m', uselib_store='m')
    ctx.check(header_name='gsl/gsl_complex.h')
    ctx.check(header_name='gsl/gsl_complex_math.h')

def build(bld):
    bld.shlib(source='poly.c', target='poly')
    bld.shlib(source='fft.c', target='fft', use=['gsl', 'm', 'cblas'])
    bld.shlib(source='integrate.c', target='integrate', use='m')

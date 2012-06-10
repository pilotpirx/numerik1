top = '.'
out = 'build'

def options(opt):
    opt.load('compiler_c')

def configure(ctx):
    ctx.load('compiler_c python')
    ctx.env.append_unique('CFLAGS_opt', '-O3')
    ctx.env.append_unique('CFLAGS_debug', '-Wall')
    ctx.env.append_unique('CFLAGS_debug', '-ggdb')
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
    bld.shlib(source='poly.c', target='poly', use='opt')
    bld.shlib(source='fft.c', target='fft', use='gsl m cblas opt')
    bld.shlib(source='integrate.c', target='integrate', use='m opt')

    bld.shlib(source='poly.c', target='poly_d', use='debug')
    bld.shlib(source='fft.c', target='fft_d', use='gsl m cblas debug')
    bld.shlib(source='integrate.c', target='integrate_d', use='debug')

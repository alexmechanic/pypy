from pypy.interpreter.error import OperationError, oefmt
from pypy.interpreter.gateway import WrappedDefault, unwrap_spec
from pypy.tool import stdlib_opcode
from pypy.interpreter.astcompiler.assemble import _opcode_stack_effect


@unwrap_spec(opcode=int)
def stack_effect(space, opcode, w_oparg=None):
    "Compute the stack effect of the opcode."
    if opcode == stdlib_opcode.EXTENDED_ARG:
        return space.newint(0)
    if opcode >= stdlib_opcode.HAVE_ARGUMENT:
        if space.is_none(w_oparg):
            raise oefmt(space.w_ValueError,
                "stack_effect: opcode requires oparg but oparg was not specified")
        oparg = space.int_w(w_oparg)
    else:
        if not space.is_none(w_oparg):
            raise oefmt(space.w_ValueError,
                "stack_effect: opcode does not permit oparg but oparg was specified")
        oparg = -1
    try:
        return space.newint(_opcode_stack_effect(opcode, oparg))
    except KeyError:
        raise oefmt(space.w_ValueError,
            "invalid opcode or oparg")

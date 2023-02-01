import inspect
import types
from typing import Any, Callable, Dict, List, Tuple, Union

from invoke.context import Context
from invoke.tasks import NO_DEFAULT, Task


def monkey_patch_invoke() -> None:

    def _patched_argspec(
        self: Any,    # pylint: disable=unused-argument
        body: Union[Callable[[Context], None], Context],
    ) -> Tuple[List[str], Dict[str, object]]:
        """
        A monkey patching code for supporting python3
        from: https://github.com/pyinvoke/invoke/issues/357#issuecomment-1250744013
        """
        signature: inspect.Signature = inspect.Signature()
        if isinstance(body, types.FunctionType):
            signature = inspect.signature(body)
        elif isinstance(body, types.MethodType):
            signature = inspect.signature(body.__call__)

        parameter_names = [name for name, _ in signature.parameters.items()]
        argument_specs: dict[str, object] = {}
        for key, value in signature.parameters.items():
            value = value.default if not value.default == signature.empty else NO_DEFAULT
            argument_specs[key] = value

        # Pop context argument
        try:
            context_arg = parameter_names.pop(0)
        except IndexError as error:
            raise TypeError('Tasks must have an initial Context argument!') from error

        del argument_specs[context_arg]
        return parameter_names, argument_specs

    Task.argspec = _patched_argspec


monkey_patch_invoke()

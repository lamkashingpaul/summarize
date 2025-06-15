from inspect import signature


def retrieve_target_from_kwargs(func, kwargs, target_name=None, target_type=None):
    sig = signature(func)
    found = None

    for name, param in sig.parameters.items():
        annotation = param.annotation
        is_name_matched = target_name is None or name == target_name
        is_type_matched = target_type is None or annotation == target_type

        if is_name_matched and is_type_matched:
            found = kwargs.get(name)
            break

    return found

class SetErrorMixin:
    def seterror(self, field, msg):
        if not self._errors.get(field, None):
            self._errors[field] = []
        self._errors[field].append(msg)
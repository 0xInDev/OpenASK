from django_filters.rest_framework.backends import DjangoFilterBackend


class APIFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        qs = super().filter_queryset(request, queryset, view)

        excludes = {param[:-1]: value for param,
                    value in request.query_params.lists() if param[-1] == '!'}
        filterset_class = self.get_filterset_class(view, qs)

        if excludes and filterset_class:
            # Update the data with excludes (other fields are kept in case they are needed in form clean)
            data = request.query_params.copy()
            for name, value in excludes.items():
                data.setlist(name, value)

            filterset = filterset_class(data=data, queryset=qs)

            # Remove redundant filters (i.e. already filtered in super)
            for name in [key for key in filterset.filters if key not in excludes]:
                filterset.filters.pop(name)

            # Invert the filters (the remaining filters are for the excluded fields)
            for name in filterset.filters:
                filterset.filters[name].exclude = not filterset.filters[name].exclude

            qs = filterset.qs

        return qs

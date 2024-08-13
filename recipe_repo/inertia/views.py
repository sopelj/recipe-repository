from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormMixin
from inertia import render

if TYPE_CHECKING:
    from typing import Any

    from django.forms import Form
    from django.http import HttpRequest, HttpResponse


class InertiaView(View):
    component: str

    def get_component_props(self) -> dict[str, Any]:
        """Fetch props for components."""
        return {}

    def get(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        """Return inertia response."""
        if not (component := self.component):
            raise ValueError("Please specify a `component` attribute.")
        response: HttpResponse = render(request, component, props=self.get_component_props())
        return response


class InertiaFormView[T](InertiaView, FormMixin[T]):  # type: ignore[valid-type,name-defined]
    """Form View Mixing to handle forms for Inertia."""

    def form_invalid(self, form: Form) -> HttpResponseRedirect:
        """In inertia, form errors are added to session and redirected back to the original page."""
        self.request.session["errors"] = form.errors
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        """Handle special form cases for inertia."""
        form = self.get_form(self.get_form_class())
        if not form.is_valid():
            # If invalid, add errors and redirect without saving.
            return HttpResponseRedirect(self.get_success_url())
        return self.form_valid(form)

from django.shortcuts import render
from django.views.generic.base import TemplateView


class MealingBaseView(TemplateView):
    """
    Base template view
    """

    context = dict()

    def get(self, request):
        return render(request, self.template_name, self.context)


class MealingIndexView(MealingBaseView):
    """
    Index view
    """
    
    template_name = 'index.html'

    def get(self, request):
        return super(MealingIndexView, self).get(request)

# Create your views here.
from django.views.generic import ListView, DetailView

from poscore.models import Tower

class TowerListView(ListView):
    model = Tower

class TowerDetailView(DetailView):
    model = Tower

    def get_context_data(self, **kwargs):
        ctx = super(TowerDetailView, self).get_context_data(**kwargs)
        ctx.update({
            'modules': self.object.modules
        })
        return ctx

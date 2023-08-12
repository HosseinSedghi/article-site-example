from django.views.generic import TemplateView

from site_module.models import SiteSetting, Links, LinkBoxes


# Create your views here.


class FooterPartial(TemplateView):
    template_name = 'includes/footer-include.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['site_data'] = SiteSetting.objects.first()
        context['link_boxes'] = LinkBoxes.objects.all()
        return context
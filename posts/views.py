from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, Process
from .forms import ServiceForm, ProcessForm
from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic import DetailView
from django.db.models import F, Sum
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.


def İndex(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def ServisList(request):
    services = Service.objects.all()

    context = {
        'services': services
    }
    return render(request, 'posts/servicelist.html', context)


@login_required(login_url='login')
def ServiceDetail(request, id):
    service = Service.objects.get(id=id)
    processes = service.action.all()
    actions = Process.objects.all()
    total = processes.aggregate(total_price=Sum(F('number') * F('price')))
    context = {
        'service': service, 'processes': processes, 'total': total, 'actions': actions}
    return render(request, 'posts/servicedetail.html', context)


@login_required(login_url='login')
def ServiceDelete(request, id):
    service = Service.objects.get(id=id)
    service.delete()
    messages.success(request, 'Servis Kaydı Silindi.')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def ServiceFormView(request):
    form = ServiceForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.full_name = request.user.profile.full_name
        post.company_name = request.user.profile.company_name
        post.phone_number = request.user.profile.phone_number
        post.save()
        messages.success(request, 'Kayıt Başarılı.')

        return redirect('index')

    return render(request, 'posts/serviceform.html', {'form': form})


@login_required(login_url='login')
def ServiceFormEditView(request, id):
    instance = get_object_or_404(Service, id=id)
    form = ServiceForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Kayıt Güncellendi.')

        return redirect('index')

    return render(request, 'posts/serviceeditform.html', {'form': form})


@login_required(login_url='login')
def MissionCompleted(request):
    service = get_object_or_404(Service, id=request.GET.get('service_id'))
    service.mission = not service.mission
    service.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def ServiceCome(request):
    service = get_object_or_404(Service, id=request.GET.get('service_id'))
    service.come = not service.come
    service.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def Delivered(request):
    service = get_object_or_404(Service, id=request.GET.get('service_id'))
    service.delivered = not service.delivered
    service.save()
    return redirect(request.META.get('HTTP_REFERER'))


class render_pdf_view(PDFTemplateResponseMixin, DetailView):
    model = Service
    template_name = 'pdf.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super(render_pdf_view, self).get_context_data(**kwargs)
        action = self.object
        context['action'] = Process.objects.filter(process=action)
        return context


@login_required(login_url='login')
def ActionAdd(request, id, action_id):
    service = get_object_or_404(Service, id=id)
    action = Process.objects.get(id=action_id)
    service.action.add(action)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def ActionDelete(request, id, action_id):
    service = get_object_or_404(Service, id=id)
    process = Process.objects.get(id=action_id, service=service)
    service.action.remove(process)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def ProcessFormView(request, id):
    form = ProcessForm(request.POST or None)
    if form.is_valid():
        process = form.save(commit=False)
        process.number = request.POST.get("number")
        process.service = Service.objects.get(id=id)
        process.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'posts/servicedetail.html', {'form': form})


@login_required(login_url='login')
def MyServiceList(request, user):
    services = Service.objects.filter(user__username=user)
    context = {
        'services': services
    }
    return render(request, 'posts/myservicelist.html', context)


@login_required(login_url='login')
def MyServiceDetail(request, id):
    service = Service.objects.get(id=id)
    processes = service.action.all()
    actions = Process.objects.all()
    total = processes.aggregate(total_price=Sum(F('number') * F('price')))
    context = {
        'service': service, 'processes': processes, 'total': total, 'actions': actions}
    return render(request, 'posts/myservicedetail.html', context)


@login_required(login_url='login')
def ServisListContinue(request):
    services = Service.objects.filter(mission=False)

    context = {
        'services': services
    }
    return render(request, 'posts/servicelistcontinue.html', context)


@login_required(login_url='login')
def ServiceDetailContinue(request, id):
    service = Service.objects.get(id=id)
    processes = service.action.all()
    actions = Process.objects.all()
    total = processes.aggregate(total_price=Sum(F('number') * F('price')))
    context = {
        'service': service, 'processes': processes, 'total': total, 'actions': actions}
    return render(request, 'posts/servicedetailcontinue.html', context)


@login_required(login_url='login')
def ServisListFinish(request):
    services = Service.objects.filter(mission=True)

    context = {
        'services': services
    }
    return render(request, 'posts/servicelistfinish.html', context)


@login_required(login_url='login')
def ServiceDetailFinish(request, id):
    service = Service.objects.get(id=id)
    processes = service.action.all()
    actions = Process.objects.all()
    total = processes.aggregate(total_price=Sum(F('number') * F('price')))
    context = {
        'service': service, 'processes': processes, 'total': total, 'actions': actions}
    return render(request, 'posts/servicedetailfinish.html', context)


@login_required(login_url='login')
def ServiceSearch(request):
    query = request.GET.get("q")
    context = {}
    if query:
        services = Service.objects.filter(
            Q(id__iexact=query),)
        context = {'services': services, }
    return render(request, 'posts/servicesearch.html', context)

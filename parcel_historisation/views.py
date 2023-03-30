from django.conf import settings
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
import json
import pathlib
import datetime

from parcel_historisation.models import Plan, Operation, OtherOperation, State, DivisonReunion


def index(request):

    user = request.META['HTTP_REMOTE_USER']
    user = user.split('\\')[1]
    user = user.lower()
    
    template = loader.get_template('parcel_historisation/index.html')
    context = {
        'user': user,
    }
    return HttpResponse(template.render(context, request))

def get_docs_list(request):
    
    numcad = request.GET["numcad"]

    results = Plan.objects.filter(state__id=1).filter(cadastre=int(numcad)).order_by('-date_plan', 'link').all()

    load = []
    for result in results:
        load.append({
            'link': result.link,
            'id': result.id,
            'designation_id': result.designation.id if result.designation else None,
        })
    first = results[0]

    if first.designation is not None:
        download = first.designation.name
    else:
        download = first.name

    return JsonResponse({
        'list': load,
        'download': download
    }, safe=False)

def file_download(request, name):

    base_path = settings.NEARCH2_CONSULTATION

    path = pathlib.Path(base_path+'/Plans_de_mutations/'+name)

    return FileResponse(open(path, 'rb'))


def get_download_path(request):

    id_ = request.GET["id"]
    type_ = request.GET["type"]

    object_ = Plan.objects.get(pk=id_)

    if type_ == 'plan':
        download_path = object_.name
    elif type_ == 'designation':
        download_path = object_.designation.name

    return  JsonResponse({
        'download_path': download_path
    }, safe=False)

def submit_saisie(request):
    
    data = json.loads(request.body)
    has_div = False
    plan = Plan.objects.get(pk=data['id'])
    
    if data["delayed_check"] is True:
      state = State.objects.get(pk=3)
      plan.state = state
      plan.save()
      return  JsonResponse({
        'submitted': False,
        'has_div': has_div
      }, safe=False)

    now = datetime.datetime.now()
    op = Operation(
        date=now,
        user=request.META['HTTP_REMOTE_USER'],
        complement=data['complement'],
        plan=plan
    )

    op.save()
    
    if data["div_check"] is True:
      div = DivisonReunion(operation=op)
      div.save()
      has_div = True

    if data["cad_check"] is True:
        other = OtherOperation(operation=op, type=1)
        other.save()

    if data["serv_check"] is True:
        other = OtherOperation(operation=op, type=2)
        other.save()
  
    if data["art35_check"] is True:
        other = OtherOperation(operation=op, type=3)
        other.save()
  
    if data["other_check"] is True:
        other = OtherOperation(operation=op, type=4)
        other.save()

    if data["cad_check"] is True:
        state = State.objects.get(pk=4)
    else:
        state = State.objects.get(pk=2)

    plan.state = state
    plan.save()

    return  JsonResponse({
        'submitted': True,
        'has_div': has_div,
    })


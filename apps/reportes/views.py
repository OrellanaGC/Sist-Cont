import os.path
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
import tempfile
from weasyprint import HTML

from django.db.models import Sum
from apps.transaccion.models import Transaccion
from apps.cuenta.models import Cuenta

import datetime
import calendar 

#from io import BytesIO
#from django.core.files.storage import FileSystemStorage
#import xhtml2pdf.pisa as pisa

# Create your views here.

def renderPdf(url_template, data={}):
    template = get_template(url_template)
    html_string = render_to_string(url_template, data)
    html = HTML(string=html_string)
    result = html.write_pdf()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="libroDiario.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response

def libroDiario(request):
    #asientos = Transaccion.models.filter
    #cuentas = Cuenta.objects.all().order_by('codigoCuenta')
    #fechaInicio = request.POST.get('fechaInicio', False)
    fechaStr = "2019-11-14"
    mes = datetime.date.today().month
    anio = datetime.date.today().year
    dias = calendar.monthrange(anio,mes)
    fechaInicio = str(anio) + "-" + ('{:02d}'.format(mes)) + "-01"
    fechaFin = str(anio) + "-" + ('{:02d}'.format(mes)) + "-" + str(dias[1])
    #if fechaInicio is not "":
    #    fecha = datetime.strptime(fechaInicio, '%d/%m/%Y')
    #    fechaStr = fecha.strftime('%Y-%m-%d')
    cuentasPadre = set()
    codCuenta = ""
    saldoDebe = 0
    saldoHaber = 0
    fechasTransacciones = set()
    transacciones = Transaccion.objects.filter(fecha__range=(fechaInicio, fechaFin)).values('cuenta__codigoCuenta', 'cuenta__cuentaPadre_id', 'cuenta__nombre', 'cuenta__tipo', 'cuenta_id', 'tipo', 'detalle', 'fecha').order_by('cuenta__codigoCuenta', 'fecha').annotate(monto = Sum('monto'))
    fechas = Transaccion.objects.filter(fecha__range=(fechaInicio, fechaFin)).values('fecha').distinct().order_by('fecha')
    for fecha in fechas:
        fechasTransacciones.add(fecha['fecha'].strftime("%d/%m/%Y"))
    for transaccion in transacciones:
        transaccion['fecha'] = transaccion['fecha'].strftime("%d/%m/%Y")
        codCuentaTransaccion = transaccion['cuenta__codigoCuenta']  
        if (not codCuenta in codCuentaTransaccion) or codCuenta == "":
            cuentasPadre.add(codCuentaTransaccion)
            codCuenta = codCuentaTransaccion
        if not "." in codCuentaTransaccion:
            if transaccion['tipo'] == 'C':
                saldoDebe += (transaccion['monto'])
            elif transaccion['tipo'] == 'A':
                saldoHaber += (transaccion['monto'])
    data = {'transacciones' : transacciones, 'cuentasPadre' : cuentasPadre, 'saldoDebe' : saldoDebe, 'saldoHaber': saldoHaber, 'fechas' : fechasTransacciones}
    pdf = renderPdf('reportes/libroDiario.html', data)
    return HttpResponse(pdf, content_type="application/pdf")

#def prueba(request):
#    response = HttpResponse(content_type="application/pdf")
#    response['Content-Disposition'] = 'attachment; filename=pruebaReporte.pdf'
#    return H
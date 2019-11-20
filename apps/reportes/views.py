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
from apps.transaccionInventario.models import TransaccionInventario

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

def libroMayor(request):
    anio = datetime.date.today().year
    fechaInicio = str(anio) + "-01-01"
    fechaFin = str(anio) + "-12-31"
    transacciones = Transaccion.objects.filter(fecha__range=(fechaInicio, fechaFin)).order_by('cuenta__codigoCuenta', 'fecha')
    cuentas = Transaccion.objects.values('cuenta_id').distinct()
    data = {'transacciones' : transacciones}
    pdf = renderPdf('reportes/libroMayor.html', data)
    return HttpResponse(pdf, content_type="application/pdf")

def kardex(request):
    #data2 = set()
    transacciones = TransaccionInventario.objects.all()
    saldos = set()
    saldo = 0
    first = True
    for transaccion in transacciones:
        if first:
            saldo = 0
            first = False
        else:
            saldo += transaccion.costoTotal
        saldos.add(saldo)
    ziplist = zip(transacciones, saldos)
    data = {'transacciones' : transacciones}
    pdf = renderPdf('reportes/kardex.html', data)
    return HttpResponse(pdf, content_type="application/pdf")

def balanceGeneral(request):
    data = {}
    pdf = renderPdf('reportes/balanceGeneral.html', data)
    return HttpResponse(pdf, content_type="application/pdf")

def estadoResultado(request):
    data = {}
    ventas = Cuenta.objects.get(codigoCuenta="51")
    costoVentas = Cuenta.objects.get(codigoCuenta="4101")
    gastosAdmin = Cuenta.objects.get(codigoCuenta="4102")
    gastosVentas = Cuenta.objects.get(codigoCuenta="4103")
    reservaLegal = Cuenta.objects.get(codigoCuenta="3102")
    impuesto = Cuenta.objects.get(codigoCuenta="2106")
    utilidadBruta = ventas.saldo - costoVentas.saldo
    gastosOperacion = gastosAdmin.saldo + gastosVentas.saldo
    uar = utilidadBruta - gastosOperacion
    uai = uar - reservaLegal.saldo
    utilidadEjercicio = uai - impuesto.saldo
    data = {'ventas' : "{0:.2f}".format(ventas.saldo), 
    'costosVentas' : "{0:.2f}".format(costoVentas.saldo), 
    'gastosOpe': "{0:.2f}".format(gastosOperacion), 
    'gastosAdmin' : "{0:.2f}".format(gastosAdmin.saldo),
    'gastosVentas' : "{0:.2f}".format(gastosVentas.saldo),
    'reservaLegal' : "{0:.2f}".format(reservaLegal.saldo),
    'impuesto' : "{0:.2f}".format(impuesto.saldo),
    'utilidadBruta' : "{0:.2f}".format(utilidadBruta), 
    'uar': "{0:.2f}".format(uar),
    'uai' : "{0:.2f}".format(uai),
    'utilidadEjercicio': "{0:.2f}".format(utilidadEjercicio)
    }
    pdf = renderPdf('reportes/estadoResultado.html', data)
    return HttpResponse(pdf, content_type="application/pdf")

def flujoEfectivo(request):
    utilidadEjercicio = getUtilidaEjercicio()
    saldo1 = Cuenta.objects.get(codigoCuenta="1202")
    depreciacion = saldo1.saldo / 5
    inventarios = Cuenta.objects.get(codigoCuenta="1105")
    ivaCredito = Cuenta.objects.get(codigoCuenta="1109")
    gastosPagados = Cuenta.objects.get(codigoCuenta="1107")
    acrededores = Cuenta.objects.get(codigoCuenta="2103")
    retenciones = Cuenta.objects.get(codigoCuenta="2104")
    ivaDebito = Cuenta.objects.get(codigoCuenta="2108")
    dividendos = Cuenta.objects.get(codigoCuenta="2110")
    cashFlow = utilidadEjercicio + depreciacion
    feo = (acrededores.saldo + retenciones.saldo + ivaDebito.saldo + dividendos.saldo) - (inventarios.saldo + ivaCredito.saldo + gastosPagados.saldo)
    fea = cashFlow + feo
    data = {'utilidadEjercicio' : "{0:.2f}".format(utilidadEjercicio),
    'depreciacion':"{0:.2f}".format(depreciacion),
    'ivaCredito':"{0:.2f}".format(ivaCredito.saldo),
    'inventarios':"{0:.2f}".format(inventarios.saldo),
    'cashFlow':"{0:.2f}".format(cashFlow),
    'feo':"{0:.2f}".format(feo),
    'gastosPagados':"{0:.2f}".format(gastosPagados.saldo),
    'ivaDebito':"{0:.2f}".format(ivaDebito.saldo),
    'retenciones':"{0:.2f}".format(retenciones.saldo),
    'dividendos':"{0:.2f}".format(dividendos.saldo),
    'acrededores':"{0:.2f}".format(acrededores.saldo),
    'fea' :"{0:.2f}".format(fea)
    }
    pdf = renderPdf('reportes/flujoEfectivo.html', data)
    return HttpResponse(pdf, content_type="application/pdf")

def getUtilidaEjercicio():
    utilidadEjercicio = 0
    ventas = Cuenta.objects.get(codigoCuenta="51")
    costoVentas = Cuenta.objects.get(codigoCuenta="4101")
    gastosAdmin = Cuenta.objects.get(codigoCuenta="4102")
    gastosVentas = Cuenta.objects.get(codigoCuenta="4103")
    reservaLegal = Cuenta.objects.get(codigoCuenta="3102")
    impuesto = Cuenta.objects.get(codigoCuenta="2106")
    utilidadBruta = ventas.saldo - costoVentas.saldo
    gastosOperacion = gastosAdmin.saldo + gastosVentas.saldo
    uar = utilidadBruta - gastosOperacion
    uai = uar - reservaLegal.saldo
    utilidadEjercicio = uai - impuesto.saldo
    return utilidadEjercicio
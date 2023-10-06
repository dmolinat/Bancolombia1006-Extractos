from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from movimiento.models import Movimiento
from cuenta.models import Cuenta
from movimiento.utils.constant import DESCRIPCIONES
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from bs4 import BeautifulSoup
import os
import PyPDF2
from django.contrib import messages


# Create your views here.
def test_hello_movement(request):
    return HttpResponse("Hola movimiento")

#Obtener los movimientos dado una cuenta.
def get_movimientos_por_cuenta(request, n_cuenta):
    movimientos = Movimiento.objects.filter(n_cuenta=n_cuenta)
    return HttpResponse(movimientos.values)
    
#Generar el extracto a partir de la cuenta, aca solo devuelve la tabla, no el archivo.
def generate_extracto(request, n_cuenta):
    if request.method=='GET':
        messages.success(request,'Identificacion válida.')
        return render(request,'generate_extracto.html')
    else:
        movimientos = Movimiento.objects.filter(n_cuenta=n_cuenta).order_by('fecha')
        
        #Calculo del saldo:
        inst_cuenta = Cuenta.objects.get(n_cuenta=n_cuenta)
        
        #Calcular saldos dado los movimientos.
        saldo_inicial=inst_cuenta.saldo
        s0=saldo_inicial
        
        list_movimientos_saldos=[]
        for movimiento in movimientos:
            #Saldo tras el movimiento
            saldo_inicial+=movimiento.valor
            
            list_movimientos_saldos.append({'fecha': movimiento.fecha,
                                            'valor': movimiento.valor,
                                            'saldo': saldo_inicial})
        
        x=render(request,'extracto.html', {'movimientos': list_movimientos_saldos, 
                                                'descripcion': DESCRIPCIONES,
                                                'saldo_inicia': s0})
        
        #String HTML
        y=list(x)[0]

        # Crear un objeto que se puede manipular como un HTML
        objeto_html = BeautifulSoup(y, 'html.parser')
        
        # Tomar la tabla del contenido
        table = objeto_html.find('table')

        # pdf auxiliar para realizar la unión.
        pdf_file = 'output.pdf'
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)

        elements = []

        # Tomar los datos de la tabla y guardarlos en una lista por filas
        data = []
        for row in table.find_all('tr'):
            data_row = []
            for cell in row.find_all(['th', 'td']):
                data_row.append(cell.get_text())
            data.append(data_row)

        # Table es una clase de Reportlab.
        pdf_table = Table(data)

        # Estilo de la tabla
        pdf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)), 
            ('TEXTCOLOR', (0, 0), (0, 0), (0, 0, 0)),  
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'), 
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
            ('BACKGROUND', (0, 1), (-1, -1), (0.95, 0.95, 0.95)),   
        ]))

        elements.append(pdf_table)

        # Generar el PDF
        doc.build(elements)
            
        # Rutas de los archivos PDF de contenido y formato estético
        pdf_contenido = 'output.pdf'
        pdf_formato = './static/Formato-Doc-Bancolombia.pdf'
        
        # Abre el PDF de contenido y el PDF de formato estético
        with open(pdf_contenido, 'rb') as pdf_content_file, open(pdf_formato, 'rb') as pdf_style_file:
            content_pdf = PyPDF2.PdfReader(pdf_content_file)
            style_pdf = PyPDF2.PdfReader(pdf_style_file)
            
            # Crea un nuevo PDF como saida
            result_pdf = PyPDF2.PdfWriter()
            
            #Contrasena: identificacion del usuario asociado a la cuenta.
            identifiacion=inst_cuenta.titular.identificacion
            
            # Combina el contenido del PDF de contenido con el formato del PDF de estilo
            for page_num in range(len(content_pdf.pages)):
                content_page = content_pdf.pages[page_num]
                style_page = style_pdf.pages[page_num]
                
                # Copia el contenido de la página de estilo (márgenes) a la página de contenido
                content_page.merge_page(style_page)
                
                # Agrega la página resultante al PDF de resultado
                result_pdf.add_page(content_page)
                
                # Contrasena     
                result_pdf.encrypt(identifiacion)    
        
        
        
            # Guarda el PDF resultante en un nuevo archivo
            output_pdf_path = os.path.join(os.path.expanduser("~"), f"Downloads\{identifiacion}_extracto_{n_cuenta}.pdf")
            with open(output_pdf_path, 'wb') as output_pdf_file:
                result_pdf.write(output_pdf_file)
            
            output_pdf_file.close()
                    
        # Ruta del archivo que deseas eliminar
        archivo_a_eliminar = 'output.pdf'

        # Verificar si el archivo existe
        if os.path.exists(archivo_a_eliminar):
            
            #Cerrar el archivo auxiliar
            pdf_content_file.close()
            
            # Eliminar el archivo
            os.remove(archivo_a_eliminar)
        else:
            print("Archivo no encontrado")
                    
        messages.success(request,f"EXTRACTO generado en la carpeta Descargas o Downloads: {output_pdf_path}.")
        messages.success(request,f"RECUERDE: Su contrasena es su numero de identificacion: {identifiacion}")
        return redirect('validar_usuario')
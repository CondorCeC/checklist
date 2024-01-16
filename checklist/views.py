from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import Group
from .models import  Questao, UserChecklist, Resposta, Avaliacao, TipoAvaliacao, Subtopico
from rest_framework import generics
from .serializers import  ChecklistAvSerializer
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import json
import pandas as pd
import re
from fpdf import FPDF
from email.mime.base import MIMEBase
from email import encoders


class ChecklistListAv(generics.ListCreateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = ChecklistAvSerializer

def home(request):
    return render(request, 'checklist/home.html')

def listar_loja(request):
    lojas = Group.objects.all()
    context = {
        'lojas':lojas,
    }
   
    return render(request, 'checklist/listar_lojas.html', context)

def checklistav(request, loja_name):
    resposta = Questao.objects.all()
    loja = get_object_or_404(Group, name=loja_name)
    tipo_avaliacao = TipoAvaliacao.objects.get()
    subtopicos = Subtopico.objects.filter(tipo_avaliacao=tipo_avaliacao)
    ultimo_subtopico = subtopicos.last() if subtopicos else None
    context = {
        'resposta':resposta,
        'loja':loja,
        'tipo_avaliacao':tipo_avaliacao,
        'subtopicos':subtopicos,
        'ultimo_subtopico': ultimo_subtopico,
    }
    return render(request, 'checklist/checklist2.html', context)

def calcular_media_subtopico(respostas):
    total = sum([resposta.resposta for resposta in respostas])
    return total / len(respostas) if respostas else 0

def salvar_avaliacao(request, loja_name):
    loja = get_object_or_404(Group, name=loja_name)
    obs = request.POST.get('comentarios')
    tipo_avaliacao = TipoAvaliacao.objects.get()
    subtopicos = Subtopico.objects.filter(tipo_avaliacao=tipo_avaliacao)
    medias_subtopicos = {}
   
    if request.method == 'POST':
        avaliacao = Avaliacao.objects.create(
        data_av=timezone.now(),
        loja=loja,
        obs=obs
    )
    
        questoes_respostas_por_subtopico = {}

        for subtopico in subtopicos:
            questoes = Questao.objects.filter(subtopico=subtopico)
            questoes_respostas = {}
            for questao in questoes:
                resposta_valor = request.POST.get(f'resposta_{questao.id}')
                if resposta_valor:
                    resposta_valor = resposta_valor.replace(',', '.')
                    Resposta.objects.create(
                        avaliacao=avaliacao,
                        questao=questao,
                        resposta=float(resposta_valor)
                    )
                    questoes_respostas[questao] = resposta_valor
            questoes_respostas_por_subtopico[subtopico] = questoes_respostas

            respostas = Resposta.objects.filter(avaliacao=avaliacao, questao__subtopico=subtopico)
            medias_subtopicos[subtopico.nome] = calcular_media_subtopico(respostas)
            media_subtopico = calcular_media_subtopico(respostas)
            medias_subtopicos[subtopico.nome] = round(media_subtopico, 1)  
            
            data_av = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        media_geral = sum(medias_subtopicos.values()) / len(medias_subtopicos) if medias_subtopicos else 0
        avaliacao.data_av = data_av
        
        
        avaliacao.media_geral = round(media_geral, 1)
        avaliacao.media_geral = media_geral
        avaliacao.medias_subtopicos = medias_subtopicos
        avaliacao.save()
        data_template = datetime.now().strftime("%d/%m/%Y")
        emails = emails_por_loja.get(loja_name)  
        gerente = gerentes_loja.get(loja_name)
        
        def extrair_digitos_loja(nome_loja):
            
            match = re.match(r'(\d{1,2})', nome_loja)
            if match:
                return match.group(1)
            else:
                return None  
        digitos_loja = extrair_digitos_loja(loja_name)
        media_ratings = ISC(digitos_loja)
       
        if emails:
            envio(gerente, obs, media_geral, loja, emails, data_template, medias_subtopicos, media_ratings, questoes_respostas_por_subtopico)
            print('Email enviado com sucesso')
        return redirect('checklist:home')  
    subtopicos = Subtopico.objects.filter(tipo_avaliacao=tipo_avaliacao).order_by('id')  
    ultimo_subtopico = subtopicos.last() if subtopicos else None
   
    context = {
        
        'subtopicos': subtopicos,
        'tipo_avaliacao': tipo_avaliacao,
        'ultimo_subtopico': ultimo_subtopico,
       
    }
    return render(request, 'checklist/home.html', context)

def login_checklist(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'Logado com sucesso como {user}!')
            return redirect('checklist:home')
        messages.error(request, 'Login inválido')
    return render(
        request,
        'checklist/login_checklist.html',
        {
            'form': form
        }
    )

def logout_checklist(request):
    auth.logout(request)
    return redirect('checklist:home')

def ISC(digitos_loja):
    url = 'https://pesquisa.cndr.me/api/feedback/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        mes_atual = datetime.now().month
        mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
        filtered_data = [item for item in data if (datetime.strptime(item['data_pedido'], '%Y-%m-%d').month in [mes_atual, mes_anterior]) and (item['loja_id'] == digitos_loja)]

        ratings = [item['rating'] for item in filtered_data]

        if ratings:
            media_ratings = sum(ratings) / len(ratings)
            media_ratings_arredondada = round(media_ratings, 1)

        else:
            print("Não há ratings disponíveis para calcular a média.")

        with open('json/pesquisa.json', 'w', encoding='utf-8') as json_file:
            json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

        df = pd.read_json('json/pesquisa.json') 
    else:
        print("Erro ao fazer a requisição") 
    return media_ratings_arredondada

def envio(gerente, obs, media_geral, loja, emails, data_template, medias_subtopicos, media_ratings, questoes_respostas_por_subtopico):
    smtp_server = 'smtp.condor.com.br'
    smtp_port = 587
    smtp_username = 'condoremcasa'
    smtp_password = '6w#b7DaT'
    #smtp_username = 'sac.cec'
    #smtp_password = 'PXGf@3PU'
    nome_loja = loja
    observacao = obs
    gerente = gerente
    media_geral = media_geral
    media_geral_arredondada = round(media_geral, 1)

    data_template=data_template
    data_formatada = data_template
    descricao_subtopicos = {
    "Separação": "Avaliado os processos de conferência do pedido (validade, quantidades, utilização das placas de gelo) e armazenamento correto dos itens.",
    "Operação de loja": "Avalia a eficácia geral das operações diárias da loja no contexto do serviço de delivery e se o responsável esta acompanhando o desempenho do time.",
    "Processos": "Analisa os procedimentos e fluxos de trabalho estabelecidos para o delivery (assinatura dos canhotos, blacklist, contato com o cliente quando necessário, sacs).",
    "Equipamentos": "Foca na qualidade e adequação dos equipamentos utilizados no delivery, como limpeza dos coolers e conservação dos celulares."
}
    medias_subtopicos_formatadas = "<ul>"
    for nome_subtopico, media in medias_subtopicos.items():
        descricao = descricao_subtopicos.get(nome_subtopico, "")
        medias_subtopicos_formatadas += f"<li>{nome_subtopico}: {media} - {descricao}</li>"
    medias_subtopicos_formatadas += "</ul>"

    conteudo_subtopicos = ""
    for subtopico, questoes_respostas in questoes_respostas_por_subtopico.items():
        conteudo_subtopicos += f"<h3>{subtopico}</h3><ul>"
        for questao, resposta in questoes_respostas.items():
            conteudo_subtopicos += f"<li>{questao} Nota aplicada: {resposta}</li>"
        conteudo_subtopicos += "</ul>"
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Detalhes da Avaliação', 0, 1, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.write_html(conteudo_subtopicos)
    pdf.output('avaliacao.pdf')
    with open('checklist/templates/checklist/template_email.html', 'r', encoding='utf-8') as file:
        template = file.read()
    template = template.replace('{{nome_loja}}', str(loja))
    template = template.replace('{{observacao}}', str(obs))
    template = template.replace('{{media_geral}}', str(media_geral_arredondada))
    template = template.replace('{{medias_subtopicos}}', medias_subtopicos_formatadas)
    template = template.replace('{{data_formatada}}', str(data_formatada))
    template = template.replace('{{media_ratings}}', str(media_ratings))
    template = template.replace('{{gerente}}', gerente)

 
    #remetente = 'Condor em Casa <sac.cec>'
    remetente = 'Condor em Casa <condoremcasa>'

    mime_multipart = MIMEMultipart()
    mime_multipart['from'] = remetente
    mime_multipart['subject'] = 'Detalhes da Avaliação'


    destinatario_principal = emails[0]
    mime_multipart['to'] = destinatario_principal

    destinatarios_copia = ', '.join(emails[1:])
    mime_multipart['cc'] = destinatarios_copia

    corpo_email = MIMEText(template, 'html', 'utf-8')
    mime_multipart.attach(corpo_email)
    attachment = open('avaliacao.pdf', 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= avaliacao.pdf")
    mime_multipart.attach(part)
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        #server.starttls() Para Gmail deixar habilitado
        server.login(smtp_username, smtp_password)
        server.send_message(mime_multipart, from_addr=remetente, to_addrs=[destinatario_principal] + emails[1:])
        print('Email enviado com sucesso')

gerentes_loja = {
    '21 - Nilo Peçanha': 'Ricardo',
    '5 - Wenceslau Braz': 'Jolsemar',
    '8 - Paranaguá': 'Luiz',
    '11 - São Braz': 'Marcos',
    '17 - Ahú Gourmet': 'Marcos',
    '22 - Champagnat': 'Vivaldo',
    '23 - Araucária': 'José',
    '27 - Novo Mundo': 'Reginaldo', 
    '29 - Água Verde': 'Robinson', 
    '31 - Campo Largo': 'Claudio',
    '32 - Ponta Grossa': 'Fabrício',
    '33 - São José dos Pinhais': 'José',   
    '37 - Cajuru': 'Marcos',
    '38 - Colombo': 'Solange',
    '43 - Almirante Tamandaré': 'Marcos',
    '50 - Santa Quitéria': 'Maurício',
    '91 - Umbará': 'Jonathan',    
}
emails_por_loja = {
    '21 - Nilo Peçanha': ['henningerik2@outlook.com',
                          'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 
                          'at2.cec@condor.com.br', 'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],
    '5 - Wenceslau Braz': ['claudinei.fitz@condor.com.br','gerencia-loja05@condor.com.br',
                       'cec.05@condor.com.br','frentecaixa-loja05@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],
    '8 - Paranaguá': ['joaocarlos@condor.com.br','gerencia-loja08@condor.com.br',
                       'cec.08@condor.com.br','frentecaixa-loja08@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],
    '11 - São Braz': ['claudinei.fitz@condor.com.br','gerencia-loja11@condor.com.br',
                       'cec.11@condor.com.br','frentecaixa-loja11@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],
    '17 - Ahú Gourmet': ['claudinei.fitz@condor.com.br','gerencia-loja17@condor.com.br',
                       'cec.17@condor.com.br','frentecaixa-loja17@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],
    # 'nilo_pecanha': ['domingos.lorenz@condor.com.br','gerencia-loja21@condor.com.br',
    #                    'cec.21@condor.com.br','frentecaixa-loja21@condor.com.br', 
    #                    'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
    #                    'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],
    '22 - Champagnat': ['domingos.lorenz@condor.com.br','gerencia-loja22@condor.com.br',
                       'cec.22@condor.com.br','frentecaixa-loja22@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],
    '23 - Araucária': ['joaocarlos@condor.com.br','gerencia-loja23@condor.com.br',
                       'cec.23@condor.com.br','frentecaixa-loja23@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],
    '27 - Novo Mundo': ['domingos.lorenz@condor.com.br','gerencia-loja27@condor.com.br',
                       'cec.27@condor.com.br','frentecaixa-loja27@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],   
    '29 - Água Verde': ['domingos.lorenz@condor.com.br','gerencia-loja29@condor.com.br',
                       'cec.29@condor.com.br','frentecaixa-loja29@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],   
    '31 - Campo Largo': ['claudinei.fitz@condor.com.br','gerencia-loja31@condor.com.br',
                       'cec.31@condor.com.br','frentecaixa-loja31@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'], 
    '32 - Ponta Grossa': ['claudinei.fitz@condor.com.br','gerencia-loja32@condor.com.br',
                       'cec.32@condor.com.br','frentecaixa-loja32@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],  
    '33 - São José dos Pinhais': ['joaocarlos@condor.com.br','gerencia-loja33@condor.com.br',
                       'cec.33@condor.com.br','frentecaixa-loja33@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],     
    '37 - Cajuru': ['joaocarlos@condor.com.br','gerencia-loja37@condor.com.br',
                       'cec.37@condor.com.br','frentecaixa-loja37@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],  
    '38 - Colombo': ['joaocarlos@condor.com.br','gerencia-loja38@condor.com.br',
                       'cec.38@condor.com.br','frentecaixa-loja38@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'], 
    '43 - Almirante Tamandaré': ['joaocarlos@condor.com.br','gerencia-loja43@condor.com.br',
                       'cec.43@condor.com.br','frentecaixa-loja43@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'], 
    '50 - Santa Quitéria': ['claudinei.fitz@condor.com.br','gerencia-loja50@condor.com.br',
                       'cec.50@condor.com.br','frentecaixa-loja50@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],  
    '91 - Umbará': ['gerenciazonta@condor.com.br','gerencia-loja91@condor.com.br',
                       'cec.91@condor.com.br','frentecaixa-loja91@condor.com.br', 
                       'condoremcasa@condor.com.br', 'rodrigo.lenz@condor.com.br', 'at2.cec@condor.com.br', 
                       'at1.cec@condor.com.br', 'tre.cec@condor.com.br'],            
}

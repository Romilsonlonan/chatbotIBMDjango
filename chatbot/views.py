from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from nltk.chat.util import Chat
from textblob import TextBlob
import nltk
from django.contrib.auth import logout
from django.contrib import auth
#from .models import Mensagem



# Inicialize a biblioteca NLTK
nltk.download('vader_lexicon')

# Listas de perguntas e respostas
pares = [
    [
        r'(.*) (Não|Negativo|De modo nehum|Assim não|Não quero!)',
        ['Desculpe, então vamos tentar novamete? Reformule a pergunta.']
    ],
    [
        r'(.*) (Não entendi|não compreendo|não entendo|não aceito)(.*?)!',
        ['Desculpe! Estou em processo de atualização. Pode reformular a pergunta?' ]
    ],
    [
        r'(.*) (Oi|Olá|Opa|Tudo bem?|Como vai você?|Como vai o seu trabalho?)',
        ['Olá Tudo bem? Em que posso ajudar?']
    ],
    [
        r'(.*?)! Show|Maravilha|Sensacional|legal|máximo|explendido|Isso é incrível|excelente (.*?)!',
        ['Fico feliz por gostar da informação!']
    ],
    [
        r'(.*) (nome?)',
        ['Meu nome é ChatBot_IBM em que posso ajudar?']
    ],  
    [
        r'(.*) idade?',
        ['Não tenho idade pois sou um chatbot']
    ], 
    [
        r'meu nome é (.*)',
        ['Olá %1, como você está hoje?']
    ],  
    [
        r'eu trabalho na empresa (.*)',
        ['Eu conheço a empresa %1']
    ], 
    [
        r'(.*) (cidade|país)',
        ['São Paulo, Brasil']
    ], 
    [
        r'(.*) (sustentabilidade)',
        ['A IBM desenvolve soluções inovadoras para melhorar a eficiência energética e promover práticas sustentáveis nas operações empresariais.']
    ], 
    [
        r'(.*)(ajudar|empresa|soluções|inovar|)',
        ['A IBM oferece uma ampla gama de soluções e serviços para ajudar empresas a inovar, crescer e se manterem competitivas. Podemos discutir opções específicas se você me der mais detalhes sobre suas necessidades.']
    ],
    [
        r'(.*) (produtos|soluções|inovar|ajudar|analise de dados|segurança cibernética|nuvel|inteligência artificial|blockchain|IBM?)',
        ['A IBM oferece uma variedade de produtos e serviços, incluindo soluções de nuvem, inteligência artificial, blockchain, análise de dados, segurança cibernética e muito mais. Posso fornecer informações mais detalhadas sobre qualquer um desses tópicos se desejar.']
    ],
    [
        r'(.*) (contato | suporte | dificuldades)',
        ['Para entrar em contato com o suporte da IBM, você pode visitar nosso site oficial e encontrar as opções de contato adequadas para o seu país ou região.']
    ],
    [
        r'(.*) (visão|criação|futuro|desenvolvimento|tecnologia|soluções)',
        ['A visão da IBM é liderar na criação, desenvolvimento e fabricação das mais avançadas tecnologias da informação, incluindo soluções de IA, nuvem e blockchain, para ajudar clientes e parceiros a resolverem os desafios mais difíceis do mundo.']
    ],
    [
        r'(.*) (benefícios|soluções|nuvem|IBM?)',
        ['As soluções em nuvem da IBM oferecem escalabilidade, segurança e flexibilidade para empresas de todos os tamanhos. Elas podem ajudar a reduzir custos, aumentar a eficiência e acelerar a inovação.']
    ],
    [
        r'(.*) (inovações|recentes|blockchain)',
        ['A IBM tem investido em áreas como inteligência artificial, computação quântica, blockchain e soluções em nuvem. Podemos discutir detalhes sobre alguma dessas inovações se você estiver interessado.']
    ],
    [
        r'(.*) (soluções|segurança)',
        ['A IBM oferece uma ampla gama de soluções de segurança cibernética, incluindo proteção contra ameaças, gerenciamento de identidade e acesso, e muito mais. Posso fornecer informações mais detalhadas se desejar.']
    ],
    [
        r'(.*) (serviços | consultoria?)',
        ['A IBM oferece serviços de consultoria em diversas áreas, incluindo transformação digital, estratégia de negócios, integração de sistemas e muito mais. Podemos discutir opções específicas se você me der mais detalhes sobre suas necessidades.']
    ],
    [
        r'(.*) (principais | principal | variedades | setores | atuação | saúde | industria | governo | finanças | IBM)',
        ['A IBM atende uma variedade de setores, incluindo finanças, saúde, indústria, governo e muitos outros. Posso fornecer informações mais detalhadas sobre como a IBM pode ajudar em seu setor específico, se desejar.']
    ],
    [
        r'quit',
        ['Até breve', 'Foi bom conversar com você. Até breve!']
    ],
    [
        r'(.*) como a IBM utiliza inteligência artificial?',
        ['A IBM aplica inteligência artificial em uma variedade de áreas, incluindo automação de processos, análise de dados avançada e assistência virtual. Posso fornecer mais detalhes se você estiver interessado.']
    ],
    [
        r'(.*) o que é o Watson da IBM?',
        ['O Watson é uma plataforma de inteligência artificial da IBM que utiliza processamento de linguagem natural e aprendizado de máquina para analisar grandes volumes de dados e fornecer insights valiosos.']
    ],
    [
        r'(.*) quais são os benefícios de usar blockchain da IBM?',
        ['A tecnologia de blockchain da IBM proporciona maior segurança e transparência em transações digitais, sendo especialmente valiosa para cadeias de suprimentos e finanças.']
    ],
    [
        r'(.*) como a IBM está contribuindo para a inovação na saúde?',
        ['A IBM desenvolve soluções avançadas para a área de saúde, incluindo análise de dados médicos, assistência virtual e ferramentas de diagnóstico.']
    ],
    [
        r'(.*) o que é a computação quântica da IBM?',
        ['A IBM está na vanguarda da pesquisa em computação quântica, desenvolvendo sistemas de processamento de informações que têm o potencial de revolucionar a computação tradicional.']
    ],
    [
        r'(.*) como a IBM lida com a segurança de dados em nuvem?',
        ['A IBM implementa medidas rigorosas de segurança em suas soluções de nuvem, incluindo criptografia avançada e sistemas de monitoramento em tempo real.']
    ],
    [
        r'(.*) quais são os serviços de suporte oferecidos pela IBM?',
        ['A IBM oferece uma variedade de serviços de suporte, incluindo assistência técnica, treinamento e consultoria especializada.']
    ],
    [
        r'(.*) como a IBM promove a sustentabilidade?',
        ['A IBM está comprometida com práticas comerciais sustentáveis, incluindo redução de emissões de carbono e o desenvolvimento de soluções ecoeficientes.']
    ],
    [
        r'(.*) qual é a visão da IBM para a IA no futuro?',
        ['A IBM acredita que a IA terá um papel central na resolução de desafios globais, desde saúde até mudanças climáticas, impulsionando a inovação e o progresso.']
    ],
    [
        r'(.*) como a IBM está envolvida com a comunidade?',
        ['A IBM apoia diversas iniciativas comunitárias e sem fins lucrativos em todo o mundo, buscando fazer um impacto positivo nas comunidades em que opera.']
    ],
    [
        r'(.*) quais são as soluções de mobilidade da IBM?',
        ['A IBM oferece soluções para gerenciamento de dispositivos móveis, aplicativos empresariais e segurança móvel para atender às necessidades das empresas modernas.']
    ],
    [
        r'(.*) como a IBM promove a diversidade e a inclusão?',
        ['A IBM está comprometida em promover a diversidade e a inclusão em seus negócios e na comunidade, trabalhando para criar ambientes inclusivos e equitativos.']
    ],
    [
        r'(.*) quais são as principais tendências tecnológicas segundo a IBM?',
        ['A IBM destaca tendências como computação quântica, automação inteligente, segurança cibernética avançada e muito mais como áreas de destaque no mundo da tecnologia.']
    ],
    [
        r'(.*) como a IBM está lidando com a transformação digital?',
        ['A IBM trabalha com empresas para fornecer soluções que impulsionem a transformação digital, incluindo estratégias de nuvem, automação e análise de dados.']
    ],
    [
        r'(.*) como a IBM está inovando na área de energia e sustentabilidade?',
        ['A IBM desenvolve soluções inovadoras para melhorar a eficiência energética e promover práticas sustentáveis nas operações empresariais.']
    ],
        [
        r'(.*) como a IBM está impulsionando a inovação em IA?',
        ['A IBM investe em pesquisa e desenvolvimento de IA, colaborando com líderes do setor e aplicando soluções avançadas em uma variedade de setores.']
    ],
    [
        r'(.*) quais são os principais eventos e conferências da IBM?',
        ['A IBM realiza uma série de eventos globais e conferências voltadas para tecnologia, inovação e negócios. Posso fornecer informações sobre eventos específicos se desejar.']
    ],
    [
        r'(.*) como a IBM apoia startups e empreendedores?',
        ['A IBM oferece programas e recursos para startups e empreendedores, incluindo acesso a tecnologias avançadas e mentoria especializada.']
    ],
    [
        r'(.*) quais são as soluções de IA da IBM para automação de processos?',
        ['A IBM oferece soluções de IA para automação de processos de negócios, ajudando empresas a otimizar operações e melhorar a eficiência.']
    ],
    [
        r'(.*) como a IBM está contribuindo para a saúde digital?',
        ['A IBM desenvolve soluções para melhorar o atendimento ao paciente, incluindo sistemas de registros médicos eletrônicos e ferramentas de análise de dados de saúde.']
    ],
    [
        r'(.*) quais são os benefícios de adotar soluções de nuvem híbrida da IBM?',
        ['A nuvem híbrida da IBM combina o melhor da nuvem pública e privada, oferecendo flexibilidade, segurança e escalabilidade para empresas.']
    ],
    [
        r'(.*) como a IBM está lidando com a segurança de dados em um mundo digital?',
        ['A IBM oferece soluções avançadas de segurança cibernética, incluindo detecção e resposta a ameaças em tempo real e gerenciamento de identidade.']
    ],
    [
        r'(.*) quais são as soluções de análise de dados oferecidas pela IBM?',
        ['A IBM fornece soluções de análise de dados avançadas para extrair insights valiosos a partir de grandes conjuntos de dados, impulsionando a tomada de decisões informadas.']
    ],
    [
        r'(.*) como a IBM está promovendo a inovação em blockchain?',
        ['A IBM desenvolve soluções de blockchain para rastreabilidade, transparência e segurança em cadeias de suprimentos, finanças e muito mais.']
    ],
    [
        r'(.*) quais são as estratégias da IBM para o uso responsável de IA?',
        ['A IBM está comprometida em desenvolver e aplicar IA de forma ética, garantindo a transparência e a responsabilidade no uso dessa tecnologia.']
    ],
    [
        r'(.*) como a IBM está abordando a transformação digital na indústria de manufatura?',
        ['A IBM oferece soluções para otimizar operações de manufatura, incluindo automação avançada, análise de dados de produção e manutenção preditiva.']
    ],
    [
        r'(.*) quais são os serviços de suporte técnico da IBM?',
        ['A IBM oferece suporte técnico especializado para ajudar empresas a resolverem problemas e manterem suas operações funcionando sem problemas.']
    ],
    [
        r'(.*) como a IBM está inovando na área de educação?',
        ['A IBM desenvolve soluções para apoiar a aprendizagem digital, incluindo plataformas de educação online e ferramentas de análise de desempenho acadêmico.']
    ],
    [
        r'(.*) quais são as iniciativas da IBM para promover a inclusão de minorias?',
        ['A IBM implementa programas e políticas para promover a diversidade e a inclusão no local de trabalho, visando criar ambientes mais equitativos e inclusivos.']
    ],
    [
        r'(.*) quais são as parcerias estratégicas da IBM com outras empresas?',
        ['A IBM colabora com uma variedade de parceiros do setor para oferecer soluções inovadoras e impulsionar a transformação digital em diversos setores.']
    ], 
    [
        r'(.*) como a IBM utiliza inteligência artificial?',
        ['A IBM aplica inteligência artificial em uma variedade de áreas, incluindo automação de processos, análise de dados avançada e assistência virtual. Posso fornecer mais detalhes se você estiver interessado.']
    ],
    [
        r'(.*) o que é o Watson da IBM?',
        ['O Watson é uma plataforma de inteligência artificial da IBM que utiliza processamento de linguagem natural e aprendizado de máquina para analisar grandes volumes de dados e fornecer insights valiosos.']
    ],
    [
        r'(.*) quais são os benefícios de usar blockchain da IBM?',
        ['A tecnologia de blockchain da IBM proporciona maior segurança e transparência em transações digitais, sendo especialmente valiosa para cadeias de suprimentos e finanças.']
    ],
    [
        r'(.*) como a IBM está contribuindo para a inovação na saúde?',
        ['A IBM desenvolve soluções avançadas para a área de saúde, incluindo análise de dados médicos, assistência virtual e ferramentas de diagnóstico.']
    ],
    [
        r'(.*) computação quântica | IBM?',
        ['A IBM está na vanguarda da pesquisa em computação quântica, desenvolvendo sistemas de processamento de informações que têm o potencial de revolucionar a computação tradicional.']
    ],
    [
        r'(.*) (segurança | dados | nuvem?)',
        ['A IBM implementa medidas rigorosas de segurança em suas soluções de nuvem, incluindo criptografia avançada e sistemas de monitoramento em tempo real.']
    ],
    [
        r'(.*) (variedade | serviços | suporte técnico | assistência técnica | consultoria | treinamento | IBM?)',
        ['A IBM oferece uma variedade de serviços de suporte, incluindo assistência técnica, treinamento e consultoria especializada.']
    ],
    [
        r'(.*) (IBM | promove | sustentável | sustentabilidade?)',
        ['A IBM está comprometida com práticas comerciais sustentáveis, incluindo redução de emissões de carbono e o desenvolvimento de soluções ecoeficientes.']
    ],
    [
        r'(.*) (visão | IBM | IA | futuro? | global | mudanças climáticas | Progresso | inovação | impulsionamento)',
        ['A IBM acredita que a IA terá um papel central na resolução de desafios globais, desde saúde até mudanças climáticas, impulsionando a inovação e o progresso.']
    ],
    [
        r'(.*) (IBM | envolvimento muldial| iniciativas | comunitária | lucrativos)',
        ['A IBM apoia diversas iniciativas comunitárias e sem fins lucrativos em todo o mundo, buscando fazer um impacto positivo nas comunidades em que opera.']
    ],
    [
        r'(.*) ( soluções | gerenciamento | Aplicativos | soluções | mobilidade | IBM)',
        ['A IBM oferece soluções para gerenciamento de dispositivos móveis, aplicativos empresariais e segurança móvel para atender às necessidades das empresas modernas.']
    ],
    [
        r'(.*) (IBM | comunidade | diversidade | inclusão?)',
        ['A IBM está comprometida em promover a diversidade e a inclusão em seus negócios e na comunidade, trabalhando para criar ambientes inclusivos e equitativos.']
    ],
    [
        r'(.*) (IBM | tendências | computação | quântica | automação | inteligente  | cibernética |tecnologia)',
        ['A IBM destaca tendências como computação quântica, automação inteligente, segurança cibernética avançada e muito mais como áreas de destaque no mundo da tecnologia.']
    ],
    [
        r'(.*) (Nuvem | Dados | Area Técnica |Integração | tecnologia | transformação digital?)',
        ['A IBM trabalha com empresas para fornecer soluções que impulsionem a transformação digital, incluindo estratégias de nuvem, automação e análise de dados.']
    ],
    [
        r'(.*) (Empresas |Inovação | área de energia | sustentabilidade?)',
        ['A IBM desenvolve soluções inovadoras para melhorar a eficiência energética e promover práticas sustentáveis nas operações empresariais.']
    ]     
]

reflections_pt = {'eu': 'você',
                  'eu sou': 'você é',
                  'eu era': 'você era',
                  "eu iria": 'você iria',
                  "eu irei": 'você irá',
                  'meu': 'seu',
                  'você': 'eu',
                  'você é': 'eu sou',
                  'você era': 'eu era',
                  "você irá": 'eu irei',
                  'seu': 'meu',
                  'minha': 'sua',
                  'meus': 'seus',
                  'suas': 'minhas',
                  'nosso': 'seu',
                  'nossa': 'sua',
                  'nossos': 'seus',
                  'nossas': 'suas',
                  'eu me sinto': 'você se sente',
                  'você se sente': 'eu me sinto',
                  'você gosta': 'eu gosto',
                  'eu gosto': 'você gosta',
                  'você pode': 'eu posso',
                  'eu posso': 'você pode',
                   'eu sei': 'você sabe',
                  'você sabe': 'eu sei',
                  'eu entendo': 'você entende',
                  'você entende': 'eu entendo',
                  'eu quero': 'você quer',
                  'você quer': 'eu quero',
                  'eu preciso': 'você precisa',
                  'você precisa': 'eu preciso',
                  'eu acho': 'você acha',
                  'você acha': 'eu acho',
                  'eu vejo': 'você vê',
                  'você vê': 'eu vejo',
                  'eu ouço': 'você ouve',
                  'você ouve': 'eu ouço',
                  'eu falo': 'você fala',
                  'você fala': 'eu falo',
                  'eu compreendo': 'você compreende',
                  'você compreende': 'eu compreendo',
                   'como são': 'como são',
                  'como é': 'como é',
                  'quais são': 'quais são',
                  'como você está': 'como eu estou',
                  'quem é você': 'quem sou eu',
                  'quem sou eu': 'quem é você',
                  'o que é isso': 'o que é aquilo',
                  'o que é aquilo': 'o que é isso',
                  'como se faz': 'como se faz',
                  'como se sente': 'como se sente',
                  'o que você quer': 'o que eu quero',
                  'o que eu quero': 'o que você quer',
                  'Obrigado!': 'Obrigado!',
                  'Muito obrigado!': 'Muito obrigado!',
                  'Agradeço muito!': 'Agradeço muito!',
                  'Fico muito agradecido(a)!': 'Fico muito agradecido(a)!',
                  'Você foi muito prestativo(a), obrigado(a)!': 'Você foi muito prestativo(a), obrigado(a)!',
                  'Não sei como agradecer o suficiente!': 'Não sei como agradecer o suficiente!',
                  'Estou muito grato(a) por isso!': 'Estou muito grato(a) por isso!',
                  'Agradeço de coração!': 'Agradeço de coração!',
                  'Obrigado(a) pela sua gentileza!': 'Obrigado(a) pela sua gentileza!',
                  'Foi muito generoso(a) da sua parte!': 'Foi muito generoso(a) da sua parte!',
                  'Obrigado(a) por tudo o que fez por mim!': 'Obrigado(a) por tudo o que fez por mim!',
                  'Estou profundamente grato(a)!': 'Estou profundamente grato(a)!',
                  'Agradeço de todo o coração!': 'Agradeço de todo o coração!',
                  'Sua ajuda foi inestimável, obrigado(a)!': 'Sua ajuda foi inestimável, obrigado(a)!',
                  'Obrigado(a) por estar sempre presente!': 'Obrigado(a) por estar sempre presente!',
                  'Agradeço pela sua consideração!': 'Agradeço pela sua consideração!',
                  'Não tenho palavras para expressar minha gratidão!': 'Não tenho palavras para expressar minha gratidão!',
                  'Sou muito grato(a) por ter você na minha vida!': 'Sou muito grato(a) por ter você na minha vida!',
                  'Seu apoio significa muito para mim, obrigado(a)!': 'Seu apoio significa muito para mim, obrigado(a)!',
                  'Não tenho como agradecer o suficiente por tudo!': 'Não tenho como agradecer o suficiente por tudo!'
                  }


# Criar uma instância do chat
chat = Chat(pares, reflections_pt)

# Pré-processamento de texto
def preprocess(text):
    return chat.respond(text)  

# Função para análise de sentimentos
def analisar_sentimento(mensagem):
    analysis = TextBlob(mensagem)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0.5:
        return "Muito positivo!"
    elif sentiment > 0:
        return "Positivo."
    elif sentiment == 0:
        return "Neutro."
    else:
        return "Negativo."
    
# Função para extrair palavras-chave
def extrair_palavras_chave(mensagem):
    tokens = nltk.word_tokenize(mensagem)
    tagged = nltk.pos_tag(tokens)
    keywords = [word for word, pos in tagged if pos in ['NN', 'VB', 'JJ']]  # Substantivos, verbos e adjetivos
    return keywords

@csrf_exempt
def chatbot(request):
    # Verifica se a solicitação é do tipo POST
    if request.method == 'POST':
        # Obtém a entrada do usuário
        user_input = request.POST.get('user_input', "")

        # Prepara a entrada do usuário para processamento
        processed_input = preprocess(user_input)

        # Percorre o dicionário de interações
        for pergunta, responder in pares:
            # Verifica se a entrada do usuário contém todas as palavras-chave da pergunta
            if processed_input is not None and all(token in processed_input for token in preprocess(pergunta)):
                # Gera uma resposta
                response_data = {'text': responder}

                # Retorna a resposta como uma resposta JSON
                return JsonResponse(response_data)

    # Se a solicitação não for POST, renderiza a página HTML
    return render(request, 'bases/chatbot.html')

# verificar o uso em uma API
#def minha_view(request):
#    if request.method == 'POST':
#        texto = request.POST.get('texto')  # Supondo que o campo de texto tenha o name="texto" no formulário
#        estrelas = request.POST.get('estrelas')  # Supondo que o campo de estrelas tenha o name="estrelas" no formulário

        # Crie uma nova instância de Mensagem com os dados recebidos
#        nova_mensagem = Mensagem(texto=texto, estrelas=estrelas)
#        nova_mensagem.save()  # Salva a mensagem no banco de dados

#        return redirect('página_sucesso')  # Redireciona para uma página de sucesso ou outra página

#    return render(request, 'sua_template.html')  # Se for um pedido GET, renderiza a página com o formulário

def exit(request):
    auth.logout(request)
    return redirect('/auth/register')






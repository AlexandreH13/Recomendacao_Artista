from math import sqrt

##Função da distância euclidiana
def distancia_euclidiana(base, user1, user2):
    si = {}
    for item in base[user1]:
        if item in base[user2]:
            si [item] = 1
    if len(si) == 0:
        return 0

    ##Faz o somatório apenas para os artistas em comum entre os usuários
    soma = sum([pow(base[user1][item] - base[user2][item],2)
                for item in base[user1] if item in base[user2]])

    return 1/(1+sqrt(soma))

###############################################################################

##Função que retorna a similaridade entre usuário
def getSimilares(base, user):
    similaridade = [(distancia_euclidiana(base, user, outro), outro)
                    for outro in base if outro != user]
    similaridade.sort()
    similaridade.reverse()
    return similaridade[0:100]

###############################################################################

##Função de recomendação
def getRecomenda(base, user):
    totais={}
    somaSimilaridades={}

    for outro in base:
        if outro == user:
            continue
        similaridade = distancia_euclidiana(base,user,outro)
        
        if similaridade <= 0:
            continue
        
        for item in base[outro]:
            ##Verifica se o artista não foi escutado pelo usuário
            if item not in base[user]:
                ##Inicializa. Key: item, valor: 0
                totais.setdefault(item,0)
                totais[item] += base[outro][item] * similaridade
                somaSimilaridades.setdefault(item,0)
                somaSimilaridades[item] += similaridade

    rankings=[(total / somaSimilaridades[item], item) for item, total in totais.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[0:100]

###############################################################################

##Carrega a base de dados
def carregaBaseDados(path='diretório da base de dados'):
    artistas={}
    for linha in open(path+'/artists.DAT',encoding='utf-8'):
        (id,nome) = linha.split('\t')[0:2]
        ##Adiciona a 'artistas' a chave 'id' e o valor 'nome'
        artistas[id] = nome

    base={}
    for linha in open(path+'/user_artists.DAT',encoding='utf-8'):
        (usuarioId,artistaId,qtd) = linha.split('\t')[0:3]
        base.setdefault(usuarioId, {})
        ##Montando a base de dados
        ##Insere a quantidade de vezes que o usuário escutou o artista
        base[usuarioId][artistas[artistaId]] = int(qtd)
    return base

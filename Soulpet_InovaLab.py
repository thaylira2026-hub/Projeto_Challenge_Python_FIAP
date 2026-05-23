import sys
import json
import os

# ---------------------------------------------------------------------------
# Arquivo json para guardar dados do usuário
# ---------------------------------------------------------------------------

ARQUIVO_DADOS = "dados_soulpet.json"

NIVEIS = (
    "Protetor Iniciante",
    "Guardião Animal",
    "Defensor da Causa",
    "Campeão dos Pets",
    "Herói Animal",
)

PONTOS_NIVEL = (0, 100, 150, 200, 250)

missoes_disponiveis = [
    {"id": 1, "descricao": "Curtir posts da comunidade",                   "pontos": 10},
    {"id": 2, "descricao": "Compartilhar campanha de adoção",              "pontos": 25},
    {"id": 3, "descricao": "Engajar com conteúdos sobre pets abandonados", "pontos": 15},
    {"id": 4, "descricao": "Indicar um amigo para a plataforma",           "pontos": 30},
    {"id": 5, "descricao": "Assistir vídeo educativo sobre pets",          "pontos": 10},
]

produtos_loja = [
    {"id": 1, "nome": "Pacote de Ração Premium",  "custo": 60},
    {"id": 2, "nome": "Brinquedo Interativo Pet", "custo": 40},
    {"id": 3, "nome": "Acessório / Coleira",      "custo": 35},
    {"id": 4, "nome": "Kit Higiene Pet",          "custo": 80},
]

ongs_cadastradas = [
    {"id": 1, "nome": "Patinhas Felizes",      "pontos_recebidos": 0},
    {"id": 2, "nome": "Resgate Pet",           "pontos_recebidos": 0},
    {"id": 3, "nome": "Anjos de Quatro Patas", "pontos_recebidos": 0},
    {"id": 4, "nome": "Amigos dos Focinhos",   "pontos_recebidos": 0},
]

# ---------------------------------------------------------------------------
# Persistência — salvar e carregar dados
# ---------------------------------------------------------------------------

def carregar_dados() -> dict:
    
    dados_padrao = {
        "usuarios": {
            "Thays Lira":              "RM568799",
            "Bianca Pereira":          "RM571077",
            "Maria Eduarda Cavallari": "RM570462",
            "Isabelle Souza":          "RM569370",
        },
        "perfis": {}
    }

    if not os.path.exists(ARQUIVO_DADOS):
        return dados_padrao

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("  Aviso: não foi possível ler o arquivo de dados. Usando dados padrão.")
        return dados_padrao


def salvar_dados(dados_globais: dict) -> None:
    """Salva todos os usuários e perfis no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados_globais, f, ensure_ascii=False, indent=2)
    except IOError:
        print("  Aviso: não foi possível salvar os dados.")


def carregar_perfil(nome: str, dados_globais: dict) -> dict:
    """Retorna o perfil salvo do usuário, ou cria um novo se não existir."""
    if nome in dados_globais["perfis"]:
        return dados_globais["perfis"][nome]
    return {
        "nome":             nome,
        "pontos":           0,
        "animais_ajudados": 0,
        "historico":        [],
    }


def salvar_perfil(dados_usuario: dict, dados_globais: dict) -> None:
    """Salva o perfil do usuário no dicionário global e grava no disco."""
    dados_globais["perfis"][dados_usuario["nome"]] = dados_usuario
    salvar_dados(dados_globais)


def separador(char: str = "-", tam: int = 50) -> None:
    print(char * tam)


def validar_inteiro(entrada: str, minimo: int, maximo: int) -> int:
    if not entrada.strip().isdigit():
        print("  Erro: Digite apenas números inteiros.")
        return -1
    valor = int(entrada.strip())
    if valor < minimo or valor > maximo:
        print(f"  Erro: Digite um número entre {minimo} e {maximo}.")
        return -1
    return valor

def calcular_nivel(pontos: int) -> str:
    nivel_atual = NIVEIS[0]
    for nivel, minimo in zip(NIVEIS, PONTOS_NIVEL):
        if pontos >= minimo:
            nivel_atual = nivel
    return nivel_atual


def pontos_proximo_nivel(pontos: int) -> str:
    for i in range(len(PONTOS_NIVEL) - 1):
        if pontos < PONTOS_NIVEL[i + 1]:
            faltam = PONTOS_NIVEL[i + 1] - pontos
            return f"Faltam {faltam} pts para '{NIVEIS[i + 1]}'"
    return "Você já atingiu o nível máximo: Herói Animal!"

def buscar_ong(ong_id: int) -> dict | None:
    for ong in ongs_cadastradas:
        if ong["id"] == ong_id:
            return ong
    return None


def buscar_produto(produto_id: int) -> dict | None:
    for produto in produtos_loja:
        if produto["id"] == produto_id:
            return produto
    return None


def menu_missoes(dados: dict, dados_globais: dict) -> None:
    separador("=")
    print("  MISSÕES DISPONÍVEIS")
    separador("=")
    for m in missoes_disponiveis:
        print(f"  [{m['id']}] {m['descricao']:<50} +{m['pontos']} pts")
    separador()

    entrada = input("  Selecione uma missão (0 para voltar): ").strip()
    opcao = validar_inteiro(entrada, 0, len(missoes_disponiveis))

    if opcao <= 0:
        return

    missao = None
    for m in missoes_disponiveis:
        if m["id"] == opcao:
            missao = m
            break

    dados["pontos"] += missao["pontos"]
    dados["historico"].append(
        f"Missão '{missao['descricao']}' concluída (+{missao['pontos']} pts)"
    )
    salvar_perfil(dados, dados_globais)  

    nivel = calcular_nivel(dados["pontos"])

    match nivel:
        case "Protetor Iniciante":
            msg = "Continue assim! Cada ação conta."
        case "Guardião Animal":
            msg = "Ótimo! Você é um Guardião Animal!"
        case "Defensor da Causa":
            msg = "Incrível! Você está defendendo a causa!"
        case "Campeão dos Pets":
            msg = "Parabéns, Campeão dos Pets!"
        case "Herói Animal":
            msg = "VOCÊ É UM HERÓI ANIMAL! Nível máximo atingido!"
        case _:
            msg = "Continue engajando!"

    print(f"\n  Missão concluída! +{missao['pontos']} pts")
    print(f"  Nível atual: {nivel} — {msg}")
    print(f"  {pontos_proximo_nivel(dados['pontos'])}")


def menu_loja(dados: dict, dados_globais: dict) -> None:
    separador("=")
    print("  LOJA SOLIDÁRIA")
    separador("=")
    print(f"  Seu saldo: {dados['pontos']} pts")
    separador()
    for p in produtos_loja:
        print(f"  [{p['id']}] {p['nome']:<30} {p['custo']} pts")
    separador()

    entrada = input("  Selecione o produto para resgatar (0 para voltar): ").strip()
    opcao = validar_inteiro(entrada, 0, len(produtos_loja))

    if opcao <= 0:
        return

    produto = buscar_produto(opcao)

    if dados["pontos"] < produto["custo"]:
        print(
            f"\n  Pontos insuficientes. Você tem {dados['pontos']} pts, "
            f"necessário {produto['custo']} pts."
        )
        return

    dados["pontos"] -= produto["custo"]
    dados["animais_ajudados"] += 1
    dados["historico"].append(f"Resgatou '{produto['nome']}' por {produto['custo']} pts")
    salvar_perfil(dados, dados_globais)  
    print(f"\n  Produto '{produto['nome']}' resgatado com sucesso!")
    print(f"  Saldo atual: {dados['pontos']} pts")


def menu_ongs(dados: dict, dados_globais: dict) -> None:
    separador("=")
    print("  ONGs PARCEIRAS")
    separador("=")
    print(f"  Seu saldo: {dados['pontos']} pts")
    separador()
    for ong in ongs_cadastradas:
        print(f"  [{ong['id']}] {ong['nome']:<30} Pts recebidos: {ong['pontos_recebidos']}")
    separador()

    entrada = input("  Escolha uma ONG para apoiar (0 para voltar): ").strip()
    opcao = validar_inteiro(entrada, 0, len(ongs_cadastradas))

    if opcao <= 0:
        return

    ong = buscar_ong(opcao)

    entrada_pts = input(f"\n  Quantos pontos deseja doar para '{ong['nome']}': ").strip()
    if not entrada_pts.isdigit():
        print("\n  Erro: Digite apenas números inteiros.")
        return

    pontos_doacao = int(entrada_pts)

    if pontos_doacao <= 0:
        print("\n  Erro: O valor da doação deve ser maior que zero.")
    elif pontos_doacao > dados["pontos"]:
        print(f"\n  Saldo insuficiente. Você tem {dados['pontos']} pts.")
    else:
        dados["pontos"] -= pontos_doacao
        dados["animais_ajudados"] += 1
        ong["pontos_recebidos"] += pontos_doacao
        dados["historico"].append(f"Doou {pontos_doacao} pts para '{ong['nome']}'")
        salvar_perfil(dados, dados_globais)  

        print(f"\n  Doação de {pontos_doacao} pts realizada para {ong['nome']}!")
        print(f"  Saldo atual: {dados['pontos']} pts")


def exibir_meu_impacto(dados: dict) -> None:
    separador("=")
    print("  PAINEL: MEU IMPACTO")
    separador("=")
    print(f"  Usuário      : {dados['nome']}")
    print(f"  Nível        : {calcular_nivel(dados['pontos'])}")
    print(f"  Pontos       : {dados['pontos']} pts")
    print(f"  Contribuições: {dados['animais_ajudados']} animais ajudados")
    separador()
    print("  Últimas ações:")
    ultimas = dados["historico"][-5:]
    if not ultimas:
        print("  Nenhuma ação registrada ainda.")
    else:
        for i, acao in enumerate(ultimas, start=1):
            print(f"    {i}. {acao}")
    separador()

def executar_comunidade_pet(dados_usuario: dict, dados_globais: dict) -> None:
    while True:
        separador("=")
        nivel = calcular_nivel(dados_usuario["pontos"])
        print(
            f"  SOUL PET  |  {dados_usuario['nome']}  "
            f"|  {nivel}  |  {dados_usuario['pontos']} pts"
        )
        separador("=")
        print("  [1] Missões")
        print("  [2] Loja Solidária")
        print("  [3] ONGs")
        print("  [4] Voltar para o app")
        separador()

        opcao = validar_inteiro(input("  Opção escolhida: ").strip(), 1, 4)
        if opcao == -1:
            continue

        match opcao:
            case 1:
                menu_missoes(dados_usuario, dados_globais)
            case 2:
                menu_loja(dados_usuario, dados_globais)
            case 3:
                menu_ongs(dados_usuario, dados_globais)
            case 4:
                print("\n  Voltando para o app Soul Up...")
                return

        exibir_meu_impacto(dados_usuario)


def navegar_abas(usuario: str, dados_globais: dict) -> None:
    while True:
        separador("=")
        print("  ABAS DO APP SOUL UP")
        separador("=")
        print("  [1] Perfil Geral")
        print("  [2] Feed de Notícias")
        print("  [3] Comunidade Soul Pet")
        print("  [4] Logout")
        separador()

        opcao = validar_inteiro(input("  Selecione uma aba: ").strip(), 1, 4)
        if opcao == -1:
            continue

        match opcao:
            case 1:
                perfil = carregar_perfil(usuario, dados_globais)
                nivel  = calcular_nivel(perfil["pontos"])
                print(f"\n  [Perfil] Usuário: {usuario} | Nível: {nivel} | {perfil['pontos']} pts")
            case 2:
                print("\n  [Feed] Parceria InovaLab traz novas metas de sustentabilidade.")
            case 3:
                separador()
                print("  Redirecionando para a Comunidade Soul Pet...")
                separador()
                dados_usuario = carregar_perfil(usuario, dados_globais)
                executar_comunidade_pet(dados_usuario, dados_globais)
            case 4:
                print(f"\n  Sessão de '{usuario}' encerrada.")
                return


def autenticar_usuario(dados_globais: dict) -> None:
    while True:
        separador("=")
        print("  BEM-VINDO À SOUL UP")
        separador("=")
        print("  [1] Fazer Login")
        print("  [2] Criar Nova Conta")
        print("  [3] Encerrar")
        separador()

        opcao = validar_inteiro(input("  Selecione uma opção: ").strip(), 1, 3)
        if opcao == -1:
            continue

        match opcao:
            case 1:
                usuario = input("\n  Usuário: ").strip()
                senha   = input("  Senha: ").strip()

                usuarios = dados_globais["usuarios"]
                if usuario in usuarios and usuarios[usuario] == senha:
                    print(f"\n  Login efetuado com sucesso! Olá, {usuario}.")
                    navegar_abas(usuario, dados_globais)
                else:
                    print("\n  Erro: Usuário ou senha incorretos.")

            case 2:
                novo_usuario = input("\n  Escolha um nome de usuário: ").strip()
                if not novo_usuario:
                    print("\n  Erro: O nome de usuário não pode ser vazio.")
                    continue
                if novo_usuario in dados_globais["usuarios"]:
                    print("\n  Erro: Este nome de usuário já está em uso.")
                    continue

                nova_senha = input("  Digite sua senha: ").strip()
                if not nova_senha:
                    print("\n  Erro: A senha não pode ser vazia.")
                    continue

                dados_globais["usuarios"][novo_usuario] = nova_senha
                salvar_dados(dados_globais)  
                print(f"\n  Conta '{novo_usuario}' criada com sucesso!")

            case 3:
                separador("=")
                print("  Fechando o aplicativo Soul Up...")
                print("  Sessão encerrada.")
                separador("=")
                sys.exit()

if __name__ == "__main__":
    print("=== PLATAFORMA SOUL UP ===")
    print("Carregando ecossistema de impacto...")

    dados_globais = carregar_dados()
    autenticar_usuario(dados_globais)
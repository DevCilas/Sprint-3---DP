# =============================================================================
# HOSPITAL SÃO RAFAEL — CRM DE VENDAS
# Sprint 3 — Recursão e Memoização
# Grupo 6
# - Cilas Pinto Macedo - RM560745
# - Ian Junji Maluvayshi Matsushita RM560588
# - Pedro Arão Baquini - RM559580
# - Leandro Kamada Pesce Dimov - RM560381
# =============================================================================

from functools import lru_cache

# -----------------------------------------------------------------------------
# DADOS DE EXEMPLO
# -----------------------------------------------------------------------------

cadastros = [
    {"id": 1, "nome": "Carlos Eduardo",  "cpf": "12345678901", "email": "carlos@email.com",   "telefone": "11987654321"},
    {"id": 2, "nome": "Ana Paula",        "cpf": "23456789012", "email": "ana@email.com",       "telefone": "11976543210"},
    {"id": 3, "nome": "João Vitor",       "cpf": "34567890123", "email": "joao@email.com",      "telefone": "11965432109"},
    {"id": 4, "nome": "Maria Fernanda",   "cpf": "45678901234", "email": "maria@email.com",     "telefone": "11954321098"},
    {"id": 5, "nome": "Luiz Henrique",    "cpf": "56789012345", "email": "luiz@email.com",      "telefone": "11943210987"},
]

novos_leads = [
    {"nome": "Carlos Eduardo",  "cpf": "12345678901", "email": "carlos@email.com",   "telefone": "11987654321"},  # duplicata total
    {"nome": "Ana Souza",       "cpf": "99999999999", "email": "ana@email.com",       "telefone": "11000000000"},  # duplicata por email
    {"nome": "Fernanda Lima",   "cpf": "11122233344", "email": "fernanda@email.com",  "telefone": "11956789012"},  # novo lead
    {"nome": "Pedro Alves",     "cpf": "56789012345", "email": "pedro@email.com",     "telefone": "11800000000"},  # duplicata por CPF
]


# =============================================================================
# TAREFA 1 — VERIFICAÇÃO RECURSIVA DE DUPLICIDADE
# =============================================================================
# A função percorre a lista de cadastros recursivamente.
# A cada chamada, compara o lead com um cadastro pelos campos principais.
# Caso base: lista percorrida sem encontrar duplicata.
# =============================================================================

def verificar_duplicidade(lead: dict, lista: list, i: int = 0) -> tuple | None:
    '''
    Percorre a lista de cadastros de forma recursiva para encontrar duplicatas
    baseadas em CPF, E-mail, Telefone ou Nome (ignorando letras maiúsculas e espaços).
    '''
    # caso base: chegou ao fim sem encontrar duplicata
    if i == len(lista):
        return None

    c = lista[i]

    campos = ["cpf", "email", "telefone", "nome"]

    for campo in campos:
        # Usamos str() para evitar erro caso o campo venha como número (int)
        v_lead = str(lead[campo]).lower().strip()
        v_cad  = str(c[campo]).lower().strip()
        
        if v_lead == v_cad:
            return (campo, c)

    return verificar_duplicidade(lead, lista, i + 1)


# =============================================================================
# TAREFA 2 — MEMOIZAÇÃO
# =============================================================================
# Usamos um dicionário de cache para guardar comparações já feitas.
# Se o par (lead, cadastro) já foi analisado, retorna o resultado salvo
# sem precisar comparar novamente.
# =============================================================================

cache = {}

def comparar_com_cache(lead: dict, cadastro: dict) -> str | None:
    '''
    Compara um lead com um cadastro específico usando um dicionário de cache (memoização). 
    Retorna o primeiro campo que causou o conflito ou None se não houver duplicidade.
    '''
    chave = (
        lead["cpf"], lead["email"], lead["telefone"], lead["nome"],
        cadastro["cpf"], cadastro["email"], cadastro["telefone"], cadastro["nome"]
    )

    if chave in cache:
        return cache[chave]  # retorna resultado salvo

    resultado = None
    campos = ["cpf", "email", "telefone", "nome"]

    for campo in campos:
        v_lead = str(lead[campo]).lower().strip()
        v_cad  = str(cadastro[campo]).lower().strip()

        if v_lead == v_cad:
            resultado = campo
            break

    cache[chave] = resultado  # salva no cache
    return resultado


def verificar_com_memoizacao(lead: dict, lista: list, i: int = 0) -> tuple | None:
    '''
    Versão otimizada da verificação de duplicidade que utiliza a função de 
    comparação com cache para evitar processamentos repetidos.
    '''
    if i == len(lista):
        return None

    campo = comparar_com_cache(lead, lista[i])
    if campo:
        return (campo, lista[i])

    return verificar_com_memoizacao(lead, lista, i + 1)


# =============================================================================
# TAREFA 3 — OTIMIZAÇÃO DE AGENDA COM SUBPROBLEMAS
# =============================================================================
# Um médico tem slots livres no dia. Cada consulta tem uma duração.
# A função calcula recursivamente quantas consultas cabem nos slots,
# usando memoização para não recalcular o mesmo estado duas vezes.


memo = {}

def encaixar_consultas(consultas: list[int], slots: list[tuple[int, int]], ic: int = 0, isl: int = 0, livre: int | None = None) -> int:
    '''
    Calcula recursivamente a quantidade máxima de consultas que podem ser encaixadas 
    nos slots do médico, usando memoização para não recalcular o mesmo cenário.
    '''
    if ic == len(consultas) or isl == len(slots):
        return 0

    inicio, fim = slots[isl]
    if livre is None:
        livre = inicio

    estado = (ic, isl, livre)
    if estado in memo:
        return memo[estado]  # resultado já calculado

    duracao = consultas[ic]
    resultado = 0

    # opção 1: encaixa a consulta
    if livre + duracao <= fim:
        resultado = max(resultado, 1 + encaixar_consultas(consultas, slots, ic + 1, isl, livre + duracao))

    # opção 2: pula para o próximo slot
    resultado = max(resultado, encaixar_consultas(consultas, slots, ic, isl + 1, None))

    # opção 3: descarta esta consulta e tenta a próxima no mesmo slot
    resultado = max(resultado, encaixar_consultas(consultas, slots, ic + 1, isl, livre))

    memo[estado] = resultado  # salva no memo
    return resultado


# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":

    # --- Tarefa 1 ---
    print("=" * 55)
    print("TAREFA 1 — VERIFICAÇÃO RECURSIVA DE DUPLICIDADE")
    print("=" * 55)

    for lead in novos_leads:
        resultado = verificar_duplicidade(lead, cadastros)
        if resultado:
            campo, conflito = resultado
            print(f"[DUPLICATA] {lead['nome']} — campo: {campo} — conflito com: {conflito['nome']}")
        else:
            print(f"[NOVO LEAD] {lead['nome']}")

    # --- Tarefa 2 ---
    print()
    print("=" * 55)
    print("TAREFA 2 — MEMOIZAÇÃO")
    print("=" * 55)

    # Primeira rodada: preenche o cache
    print("1ª rodada (preenche cache):")
    for lead in novos_leads:
        verificar_com_memoizacao(lead, cadastros)
    print(f"  Entradas no cache após 1ª rodada: {len(cache)}")

    # Segunda rodada: tudo vem do cache
    print("2ª rodada (usa cache):")
    for lead in novos_leads:
        verificar_com_memoizacao(lead, cadastros)
    print(f"  Entradas no cache após 2ª rodada: {len(cache)} (sem crescimento = cache funcionando)")

    # --- Tarefa 3 ---
    print()
    print("=" * 55)
    print("TAREFA 3 — OTIMIZAÇÃO DE AGENDA")
    print("=" * 55)

    # Slots do médico: (início, fim) em minutos — ex: 480 = 08:00
    slots = [
        (480, 600),  # 08:00 – 10:00
        (660, 780),  # 11:00 – 13:00
        (840, 960),  # 14:00 – 16:00
    ]

    consultas = [30, 45, 60, 20, 30, 50, 40]  # durações em minutos

    print(f"Slots disponíveis : 08:00–10:00 | 11:00–13:00 | 14:00–16:00")
    print(f"Consultas pedidas : {consultas} minutos")

    memo.clear()
    total = encaixar_consultas(consultas, slots)

    print(f"Máximo de consultas encaixadas: {total} de {len(consultas)}")
    print(f"Estados memoizados: {len(memo)}")
from pathlib import Path

DIRETORIO_PROJETOS = Path("/home/mfsever/compartilhado/estudos-ia")
DIAS_ANALISADOS = 7
MODELO = "qwen3.8:27b"
CONTEXTO = 16384
MODELO_EXTRACAO = "qwen3.8:27b"
MODELO_REDACAO = "qwen3.8:27b"
DIRETORIO_ESTILO = Path(__file__).parent / "estilo"
DIRETORIO_RASCUNHOS = Path(__file__).parent / "rascunhos"
VARIACOES = 3
ANGULOS = (
    "Conte a semana como uma jornada de construção: o que foi feito e por quê.",
    "Foque na descoberta mais surpreendente e explique-a bem.",
    "Foque nas limitações e riscos encontrados, e no que você fará a respeito.",
)
MAX_EXEMPLOS = 5
#!/usr/bin/env bash
#
# Sobe o SonarQube local, gera o token e executa a análise do Banco Digital.
#
# Uso:
#   ./scripts/sonar_local.sh up
#   ./scripts/sonar_local.sh bootstrap
#   ./scripts/sonar_local.sh scan
#   ./scripts/sonar_local.sh status
#   ./scripts/sonar_local.sh down
#   ./scripts/sonar_local.sh reset
#
# Requisitos: Docker + Docker Compose, uv, curl e jq.
# O sonar-scanner é opcional: se não estiver instalado, o script usa a imagem
# oficial do scanner via Docker.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SONAR_URL="${SONAR_URL:-http://localhost:9000}"
SONAR_PROJECT_KEY="${SONAR_PROJECT_KEY:-banco-digital-uff-2026-2}"
SONAR_ADMIN_USER="${SONAR_ADMIN_USER:-admin}"
SONAR_ADMIN_PASSWORD="${SONAR_ADMIN_PASSWORD:-admin}"
SONAR_TOKEN_FILE="${SONAR_TOKEN_FILE:-$ROOT_DIR/.sonar/token}"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT_DIR/docker-compose.yml}"

info() { printf '\033[1;34m[sonar]\033[0m %s\n' "$*" >&2; }
warn() { printf '\033[1;33m[sonar]\033[0m %s\n' "$*" >&2; }
die() { printf '\033[1;31m[sonar]\033[0m %s\n' "$*" >&2; exit 1; }

need_cmd() {
    command -v "$1" >/dev/null 2>&1 || die "Comando '$1' não encontrado."
}

compose() {
    docker compose -f "$COMPOSE_FILE" "$@"
}

sonar_status() {
    curl -fsS "$SONAR_URL/api/system/status" 2>/dev/null | grep -q '"status":"UP"'
}

wait_up() {
    need_cmd curl
    info "Aguardando SonarQube em $SONAR_URL ..."
    for _ in $(seq 1 90); do
        if sonar_status; then
            info "SonarQube UP."
            return 0
        fi
        sleep 2
    done
    die "SonarQube não ficou UP. Veja: docker compose -f $COMPOSE_FILE logs sonarqube"
}

token_valid() {
    local token="${1:-}"
    [ -n "$token" ] || return 1
    curl -fsS -H "Authorization: Bearer $token" \
        "$SONAR_URL/api/authentication/validate" 2>/dev/null | grep -q '"valid":true'
}

read_token() {
    if [ -n "${SONAR_TOKEN:-}" ]; then
        printf '%s' "$SONAR_TOKEN"
        return 0
    fi
    if [ -f "$SONAR_TOKEN_FILE" ]; then
        cat "$SONAR_TOKEN_FILE"
        return 0
    fi
    return 1
}

generate_token() {
    need_cmd curl
    need_cmd jq
    local response token
    info "Gerando token em $SONAR_URL (usuário: $SONAR_ADMIN_USER)..."
    response="$(curl -fsS -u "$SONAR_ADMIN_USER:$SONAR_ADMIN_PASSWORD" \
        -X POST "$SONAR_URL/api/user_tokens/generate?name=entrega-2-$(date +%Y%m%d-%H%M%S)")" \
        || die "Falha ao gerar token. Verifique SONAR_ADMIN_USER/SONAR_ADMIN_PASSWORD."
    token="$(printf '%s' "$response" | jq -r '.token // empty')"
    [ -n "$token" ] || die "SonarQube não retornou token: $response"
    mkdir -p "$(dirname "$SONAR_TOKEN_FILE")"
    printf '%s' "$token" > "$SONAR_TOKEN_FILE"
    chmod 600 "$SONAR_TOKEN_FILE"
    info "Token salvo em $SONAR_TOKEN_FILE (ignorado pelo Git)."
    printf '%s' "$token"
}

ensure_token() {
    local token
    token="$(read_token 2>/dev/null || true)"
    if token_valid "$token"; then
        printf '%s' "$token"
        return 0
    fi
    if [ -n "$token" ]; then
        warn "Token existente inválido; gerando outro."
    fi
    generate_token
}

bootstrap_profile() {
    local token="$1"
    need_cmd curl
    info "Associando o projeto '$SONAR_PROJECT_KEY' ao perfil 'Sonar way comprehensive'..."
    if curl -fsS -H "Authorization: Bearer $token" \
        -X POST \
        --data-urlencode 'qualityProfile=Sonar way comprehensive' \
        --data-urlencode 'language=py' \
        --data-urlencode "project=$SONAR_PROJECT_KEY" \
        "$SONAR_URL/api/qualityprofiles/add_project" >/dev/null; then
        info "Perfil Python associado."
    else
        warn "Não foi possível associar o perfil (pode já estar associado ou não existir nesta versão)."
    fi
}

cmd_up() {
    need_cmd docker
    docker compose version >/dev/null 2>&1 || die "Docker Compose não está disponível."
    info "Subindo SonarQube..."
    compose up -d
    wait_up
    info "Acesse $SONAR_URL (admin/admin na primeira execução)."
}

cmd_down() {
    need_cmd docker
    compose down
    info "Container parado. Volumes preservados."
}

cmd_reset() {
    need_cmd docker
    warn "Isso remove o container E os volumes do SonarQube (histórico de análises)."
    read -r -p "Digite 'reset' para confirmar: " answer
    [ "$answer" = "reset" ] || { info "Cancelado."; exit 0; }
    compose down -v
    info "SonarQube e volumes removidos."
}

cmd_status() {
    if sonar_status; then
        info "SonarQube UP em $SONAR_URL (projeto: $SONAR_PROJECT_KEY)."
    else
        warn "SonarQube não respondeu em $SONAR_URL."
        exit 1
    fi
}

cmd_token() {
    ensure_token
    printf '\n'
}

cmd_bootstrap() {
    cmd_up
    local token
    token="$(ensure_token)"
    bootstrap_profile "$token"
    info "Pronto. Rode: ./scripts/sonar_local.sh scan"
}

run_scanner() {
    local token="$1"
    if command -v sonar-scanner >/dev/null 2>&1; then
        sonar-scanner -Dsonar.host.url="$SONAR_URL" -Dsonar.token="$token"
        return
    fi

    need_cmd docker
    warn "sonar-scanner não encontrado; usando a imagem oficial via Docker."
    local host_url="$SONAR_URL"
    host_url="${host_url/localhost/host.docker.internal}"
    local -a docker_cmd=(
        docker run --rm
        -v "$ROOT_DIR:/usr/src"
        -w /usr/src
        -e "SONAR_HOST_URL=$host_url"
        -e "SONAR_TOKEN=$token"
    )
    if [ "$(uname -s)" = "Linux" ]; then
        docker_cmd+=(--add-host=host.docker.internal:host-gateway)
    fi
    docker_cmd+=(sonarsource/sonar-scanner-cli:latest)
    "${docker_cmd[@]}"
}

cmd_scan() {
    need_cmd uv
    local token pytest_exit=0
    if ! sonar_status; then
        warn "SonarQube não está UP; rode './scripts/sonar_local.sh up' primeiro."
        exit 1
    fi
    token="$(ensure_token)"
    info "Gerando coverage.xml..."
    uv run pytest tests/unit --cov=app --cov-branch --cov-report=xml \
        --cov-fail-under=0 || pytest_exit=$?
    [ -f coverage.xml ] || die "coverage.xml não foi gerado."
    run_scanner "$token"
    if [ "$pytest_exit" -ne 0 ]; then
        warn "A análise foi enviada, mas o pytest terminou com código $pytest_exit (falhas registradas)."
    fi
    exit "$pytest_exit"
}

usage() {
    cat <<'EOF'
Uso: scripts/sonar_local.sh <comando>

Comandos:
  up         Sobe o SonarQube local e aguarda ficar UP
  down       Para o container (mantém os volumes)
  reset      Remove container e volumes (apaga o histórico)
  status     Mostra se o SonarQube está UP
  bootstrap  Sobe, gera token e associa o perfil Python
  token      Imprime o token atual (gera um se necessário)
  scan       Gera coverage.xml e executa o sonar-scanner

Variáveis:
  SONAR_URL               default http://localhost:9000
  SONAR_PROJECT_KEY       default banco-digital-uff-2026-2
  SONAR_ADMIN_USER        default admin
  SONAR_ADMIN_PASSWORD    default admin (troque se já alterou a senha)
  SONAR_TOKEN             se definido, tem prioridade sobre .sonar/token
  SONAR_TOKEN_FILE        default .sonar/token

Observação: o token fica em .sonar/token, que está no .gitignore.
EOF
}

case "${1:-}" in
    up) cmd_up ;;
    down) cmd_down ;;
    reset) cmd_reset ;;
    status) cmd_status ;;
    bootstrap) cmd_bootstrap ;;
    token) cmd_token ;;
    scan) cmd_scan ;;
    ""|-h|--help|help) usage ;;
    *) usage; exit 1 ;;
esac

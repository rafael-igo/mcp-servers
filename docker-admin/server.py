#!/usr/bin/env python3
"""
Docker Admin MCP
================
Gerenciamento automático de Docker, MCPs e API.
Auto-healing, monitoramento e controle completo da infraestrutura.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("docker-admin")

# Paths
MCP_SERVERS_DIR = Path("/project/api/mcp-servers")
API_DIR = Path("/project/api")
DOCS_DIR = Path("/app/docs")
MCP_CONFIG_FILE = Path("/project/.mcp.json")


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> Dict:
    """Executa comando e retorna resultado."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or MCP_SERVERS_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Comando timeout após 30s"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def check_docker_status() -> str:
    """
    Verifica se Docker está rodando e tenta iniciar se necessário.

    Returns:
        JSON com status do Docker e ação tomada
    """
    try:
        # Verificar se Docker está rodando
        result = run_command(["docker", "info"])

        if result["success"]:
            return json.dumps({
                "success": True,
                "status": "running",
                "message": "Docker está rodando normalmente"
            }, indent=2)

        # Tentar iniciar Docker (macOS)
        start_result = run_command(["open", "-a", "Docker"])

        if start_result["success"]:
            import time
            time.sleep(5)  # Aguardar Docker iniciar

            # Verificar novamente
            verify = run_command(["docker", "info"])
            if verify["success"]:
                return json.dumps({
                    "success": True,
                    "status": "started",
                    "message": "Docker foi iniciado com sucesso"
                }, indent=2)

        return json.dumps({
            "success": False,
            "status": "failed",
            "error": "Não foi possível iniciar o Docker",
            "details": result["stderr"]
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def manage_mcps(action: str) -> str:
    """
    Gerencia todos os MCPs de uma vez.

    Args:
        action: start | stop | restart | rebuild | status

    Returns:
        JSON com resultado da operação
    """
    try:
        # Verificar Docker primeiro
        docker_check = json.loads(check_docker_status())
        if not docker_check.get("success"):
            return json.dumps({
                "success": False,
                "error": "Docker não está disponível",
                "details": docker_check
            }, indent=2)

        commands = {
            "start": ["docker-compose", "up", "-d"],
            "stop": ["docker-compose", "stop"],
            "restart": ["docker-compose", "restart"],
            "rebuild": ["docker-compose", "up", "-d", "--build"],
            "status": ["docker-compose", "ps"]
        }

        if action not in commands:
            return json.dumps({
                "success": False,
                "error": f"Ação inválida: {action}",
                "valid_actions": list(commands.keys())
            }, indent=2)

        result = run_command(commands[action])

        return json.dumps({
            "success": result["success"],
            "action": action,
            "output": result["stdout"],
            "error": result["stderr"] if not result["success"] else None
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def manage_mcp(name: str, action: str) -> str:
    """
    Gerencia um MCP específico.

    Args:
        name: Nome do MCP (ex: excel-server, agente-orchestrator)
        action: start | stop | restart | rebuild | logs

    Returns:
        JSON com resultado da operação
    """
    try:
        if action == "logs":
            result = run_command(["docker-compose", "logs", "--tail=50", name])
        elif action == "restart":
            result = run_command(["docker-compose", "restart", name])
        elif action == "stop":
            result = run_command(["docker-compose", "stop", name])
        elif action == "start":
            result = run_command(["docker-compose", "up", "-d", name])
        elif action == "rebuild":
            result = run_command(["docker-compose", "up", "-d", "--build", name])
        else:
            return json.dumps({
                "success": False,
                "error": f"Ação inválida: {action}",
                "valid_actions": ["start", "stop", "restart", "rebuild", "logs"]
            }, indent=2)

        return json.dumps({
            "success": result["success"],
            "mcp": name,
            "action": action,
            "output": result["stdout"],
            "error": result["stderr"] if not result["success"] else None
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def manage_api(action: str) -> str:
    """
    Gerencia a API do projeto.

    Args:
        action: start | stop | restart | rebuild | status | logs

    Returns:
        JSON com resultado da operação
    """
    try:
        # Verificar se há docker-compose na API
        api_compose = API_DIR / "docker-compose.yml"

        if not api_compose.exists():
            return json.dumps({
                "success": False,
                "error": "API não possui docker-compose.yml",
                "note": "Use comandos npm/node diretamente"
            }, indent=2)

        commands = {
            "start": ["docker-compose", "up", "-d"],
            "stop": ["docker-compose", "stop"],
            "restart": ["docker-compose", "restart"],
            "rebuild": ["docker-compose", "up", "-d", "--build"],
            "status": ["docker-compose", "ps"],
            "logs": ["docker-compose", "logs", "--tail=50"]
        }

        if action not in commands:
            return json.dumps({
                "success": False,
                "error": f"Ação inválida: {action}",
                "valid_actions": list(commands.keys())
            }, indent=2)

        result = run_command(commands[action], cwd=API_DIR)

        return json.dumps({
            "success": result["success"],
            "action": action,
            "output": result["stdout"],
            "error": result["stderr"] if not result["success"] else None
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def health_check() -> str:
    """
    Verifica saúde de toda infraestrutura e tenta auto-corrigir problemas.

    Returns:
        JSON com status completo e ações tomadas
    """
    try:
        report = {
            "timestamp": subprocess.run(
                ["date", "+%Y-%m-%d %H:%M:%S"],
                capture_output=True,
                text=True
            ).stdout.strip(),
            "docker": {},
            "mcps": {},
            "api": {},
            "actions_taken": []
        }

        # 1. Verificar Docker
        docker_result = run_command(["docker", "info"])
        report["docker"]["running"] = docker_result["success"]

        if not docker_result["success"]:
            report["actions_taken"].append("Docker não está rodando - tentando iniciar...")
            check_result = json.loads(check_docker_status())
            report["docker"]["auto_start"] = check_result.get("success", False)

        # 2. Verificar MCPs
        mcps_status = run_command(["docker-compose", "ps"])
        if mcps_status["success"]:
            # Parsear containers
            lines = mcps_status["stdout"].strip().split('\n')
            for line in lines[1:]:  # Pular header
                if "Up" in line:
                    container_name = line.split()[0]
                    report["mcps"][container_name] = "running"
                elif line.strip():
                    container_name = line.split()[0]
                    report["mcps"][container_name] = "stopped"

                    # Auto-heal: tentar iniciar containers parados
                    report["actions_taken"].append(f"Container {container_name} parado - reiniciando...")
                    restart = run_command(["docker-compose", "up", "-d", container_name])
                    if restart["success"]:
                        report["mcps"][container_name] = "restarted"

        # 3. Verificar API
        api_compose = API_DIR / "docker-compose.yml"
        if api_compose.exists():
            api_status = run_command(["docker-compose", "ps"], cwd=API_DIR)
            report["api"]["has_compose"] = True
            report["api"]["running"] = "Up" in api_status["stdout"]
        else:
            report["api"]["has_compose"] = False
            report["api"]["note"] = "API não usa Docker Compose"

        report["success"] = True
        report["overall_health"] = "healthy" if not report["actions_taken"] else "recovered"

        return json.dumps(report, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def get_logs(service: str, lines: int = 50) -> str:
    """
    Obtém logs de um serviço específico.

    Args:
        service: Nome do serviço/container
        lines: Número de linhas (padrão: 50)

    Returns:
        JSON com os logs
    """
    try:
        result = run_command(["docker-compose", "logs", f"--tail={lines}", service])

        return json.dumps({
            "success": result["success"],
            "service": service,
            "lines": lines,
            "logs": result["stdout"],
            "error": result["stderr"] if not result["success"] else None
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def auto_heal() -> str:
    """
    Executa auto-healing completo:
    - Verifica Docker e inicia se necessário
    - Detecta containers parados e reinicia
    - Verifica saúde e corrige problemas

    Returns:
        JSON com relatório completo de ações
    """
    try:
        actions = []

        # 1. Garantir Docker está rodando
        docker_check = json.loads(check_docker_status())
        if docker_check.get("status") == "started":
            actions.append({
                "action": "start_docker",
                "status": "success",
                "message": "Docker foi iniciado"
            })

        # 2. Health check completo
        health = json.loads(health_check())
        if health.get("success"):
            actions.extend([
                {
                    "action": "health_check",
                    "status": "success",
                    "details": health
                }
            ])

        # 3. Verificar se há containers com erro
        ps_result = run_command(["docker-compose", "ps"])
        if "Restarting" in ps_result["stdout"] or "Exit" in ps_result["stdout"]:
            actions.append({
                "action": "rebuild_failed_containers",
                "status": "in_progress",
                "message": "Detectados containers com falha - fazendo rebuild..."
            })

            rebuild = json.loads(manage_mcps("rebuild"))
            actions.append({
                "action": "rebuild_failed_containers",
                "status": "success" if rebuild.get("success") else "failed",
                "details": rebuild
            })

        return json.dumps({
            "success": True,
            "timestamp": subprocess.run(
                ["date", "+%Y-%m-%d %H:%M:%S"],
                capture_output=True,
                text=True
            ).stdout.strip(),
            "actions_taken": actions,
            "message": f"Auto-healing completo. {len(actions)} ações executadas."
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def get_mcp_status() -> str:
    """
    Retorna status completo dos MCPs (containers + configuração).

    Returns:
        JSON com status de containers e configuração
    """
    try:
        # 1. Status dos containers
        ps_result = run_command(["docker-compose", "ps", "--format", "json"])

        containers = {}
        if ps_result["success"] and ps_result["stdout"]:
            for line in ps_result["stdout"].strip().split('\n'):
                try:
                    container = json.loads(line)
                    name = container.get("Name", "").replace("igo-", "")
                    containers[name] = {
                        "state": container.get("State", "unknown"),
                        "status": container.get("Status", "unknown")
                    }
                except json.JSONDecodeError:
                    pass

        # 2. Status da configuração
        config_status = {
            "exists": MCP_CONFIG_FILE.exists(),
            "servers": []
        }

        if MCP_CONFIG_FILE.exists():
            with open(MCP_CONFIG_FILE, 'r') as f:
                config = json.load(f)
                config_status["servers"] = list(config.get("mcpServers", {}).keys())

        # 3. Verificar sincronização
        sync_issues = []
        for container_name in containers.keys():
            if container_name not in config_status["servers"]:
                sync_issues.append(f"Container '{container_name}' rodando mas não configurado em .mcp.json")

        for server_name in config_status["servers"]:
            if server_name not in containers:
                sync_issues.append(f"Server '{server_name}' configurado mas container não está rodando")

        return json.dumps({
            "success": True,
            "containers": containers,
            "config": config_status,
            "sync_issues": sync_issues,
            "is_synced": len(sync_issues) == 0
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def sync_mcp_config() -> str:
    """
    Sincroniza o arquivo .mcp.json com os containers em execução.
    Atualiza automaticamente a configuração com todos os MCPs rodando.

    Returns:
        JSON confirmando sincronização
    """
    try:
        # 1. Obter lista de containers MCP rodando
        ps_result = run_command(["docker-compose", "ps", "--format", "json"])

        if not ps_result["success"]:
            return json.dumps({
                "success": False,
                "error": "Não foi possível listar containers",
                "details": ps_result["stderr"]
            }, indent=2)

        # 2. Parsear containers
        running_mcps = []
        if ps_result["stdout"]:
            for line in ps_result["stdout"].strip().split('\n'):
                try:
                    container = json.loads(line)
                    name = container.get("Name", "")
                    if name.startswith("igo-") and container.get("State") == "running":
                        mcp_name = name.replace("igo-", "")
                        running_mcps.append(mcp_name)
                except json.JSONDecodeError:
                    pass

        if not running_mcps:
            return json.dumps({
                "success": False,
                "error": "Nenhum container MCP em execução",
                "note": "Inicie os containers primeiro com manage_mcps('start')"
            }, indent=2)

        # 3. Construir nova configuração
        new_config = {
            "mcpServers": {}
        }

        for mcp_name in running_mcps:
            container_name = f"igo-{mcp_name}"
            new_config["mcpServers"][mcp_name] = {
                "type": "stdio",
                "command": "docker",
                "args": ["exec", "-i", container_name, "python", "server.py"],
                "env": {
                    "PYTHONUNBUFFERED": "1"
                }
            }

        # 4. Salvar configuração
        with open(MCP_CONFIG_FILE, 'w') as f:
            json.dump(new_config, f, indent=2)

        return json.dumps({
            "success": True,
            "message": f"Configuração .mcp.json atualizada com {len(running_mcps)} MCPs",
            "mcps_configured": running_mcps,
            "config_path": str(MCP_CONFIG_FILE)
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def verify_mcp_config() -> str:
    """
    Verifica se o arquivo .mcp.json está sincronizado com os containers.

    Returns:
        JSON com resultado da verificação
    """
    try:
        # Usar get_mcp_status para verificar
        status = json.loads(get_mcp_status())

        if not status.get("success"):
            return json.dumps(status, indent=2)

        sync_issues = status.get("sync_issues", [])

        result = {
            "success": True,
            "is_synced": len(sync_issues) == 0,
            "containers_count": len(status.get("containers", {})),
            "configured_count": len(status.get("config", {}).get("servers", [])),
            "issues": sync_issues
        }

        if not result["is_synced"]:
            result["recommendation"] = "Execute sync_mcp_config() para sincronizar"

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
def update_and_restart_mcps() -> str:
    """
    Sequência completa de atualização:
    1. Para containers
    2. Reconstrói imagens
    3. Inicia containers
    4. Sincroniza .mcp.json

    Returns:
        JSON com resultado de cada etapa
    """
    try:
        actions = []

        # 1. Parar containers
        actions.append({
            "step": "stop",
            "message": "Parando containers..."
        })
        stop_result = json.loads(manage_mcps("stop"))
        actions.append({
            "step": "stop",
            "success": stop_result.get("success"),
            "details": stop_result
        })

        if not stop_result.get("success"):
            return json.dumps({
                "success": False,
                "error": "Falha ao parar containers",
                "actions": actions
            }, indent=2)

        # 2. Rebuild
        actions.append({
            "step": "rebuild",
            "message": "Reconstruindo imagens..."
        })
        rebuild_result = json.loads(manage_mcps("rebuild"))
        actions.append({
            "step": "rebuild",
            "success": rebuild_result.get("success"),
            "details": rebuild_result
        })

        if not rebuild_result.get("success"):
            return json.dumps({
                "success": False,
                "error": "Falha ao reconstruir imagens",
                "actions": actions
            }, indent=2)

        # 3. Aguardar containers estarem prontos
        import time
        time.sleep(3)

        # 4. Sincronizar config
        actions.append({
            "step": "sync_config",
            "message": "Sincronizando .mcp.json..."
        })
        sync_result = json.loads(sync_mcp_config())
        actions.append({
            "step": "sync_config",
            "success": sync_result.get("success"),
            "details": sync_result
        })

        return json.dumps({
            "success": True,
            "message": "✅ MCPs atualizados, reiniciados e configurados com sucesso!",
            "actions": actions,
            "mcps_configured": sync_result.get("mcps_configured", [])
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

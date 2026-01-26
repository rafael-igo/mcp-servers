# SSH no Windows (OpenSSH) - Chaves autorizadas

Este guia mostra como configurar autenticação por chave no Windows para o MCP via SSH.

## 1) Pré-requisitos

- OpenSSH Server instalado e rodando no Windows.
- Acesso como administrador no Windows.
- Chave pública gerada no cliente (linha `ssh-ed25519 ...`).

## 2) Identificar o usuário correto

Se o SSH conecta como `rafael@15.15.255.9`, o usuário no Windows é `rafael`.
As chaves precisam ficar no local desse usuário.

## 3) Colocar a chave pública

### 3.1) Se o usuário NÃO é administrador

Arquivo: `C:\Users\SEU_USUARIO\.ssh\authorized_keys`

```powershell
mkdir $env:USERPROFILE\.ssh -Force
notepad $env:USERPROFILE\.ssh\authorized_keys
```

Cole a linha `ssh-ed25519 ...` (uma linha só) e salve.

### 3.2) Se o usuário é administrador

Se o `sshd_config` tiver:

```
Match Group administrators
    AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

então use este arquivo:

```powershell
New-Item -ItemType File -Path C:\ProgramData\ssh\administrators_authorized_keys -Force
notepad C:\ProgramData\ssh\administrators_authorized_keys
```

Cole a linha `ssh-ed25519 ...` e salve.

## 4) Permissoes corretas (obrigatorio)

### 4.1) Para `authorized_keys` do usuario

```powershell
icacls $env:USERPROFILE\.ssh /inheritance:r
icacls $env:USERPROFILE\.ssh /grant "SEU_USUARIO:(OI)(CI)F" /grant "SYSTEM:(OI)(CI)F" /grant "*S-1-5-32-544:(OI)(CI)F"

icacls $env:USERPROFILE\.ssh\authorized_keys /inheritance:r
icacls $env:USERPROFILE\.ssh\authorized_keys /grant "SEU_USUARIO:F" /grant "SYSTEM:F" /grant "*S-1-5-32-544:F"
```

### 4.2) Para `administrators_authorized_keys`

```powershell
icacls C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r
icacls C:\ProgramData\ssh\administrators_authorized_keys /grant "SYSTEM:F" /grant "*S-1-5-32-544:F"
```

Reinicie o serviço:

```powershell
Restart-Service sshd
```

## 5) Verificar do cliente (Mac/Linux)

```bash
ssh SEU_USUARIO@IP_DO_SERVIDOR
```

Se pedir senha, o servidor nao aceitou a chave.

## 6) Erros comuns

- Usuario errado: a chave foi salva em outro perfil.
- `authorized_keys` com quebra de linha no meio da chave.
- Permissoes incorretas no arquivo/pasta.
- Usuario admin usando o arquivo errado (`administrators_authorized_keys`).

## 7) Logs do OpenSSH

```powershell
Get-Content C:\ProgramData\ssh\logs\sshd.log -Tail 200
```

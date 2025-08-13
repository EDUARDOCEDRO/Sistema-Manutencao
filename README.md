# Sistema de Manutenção Automatizada para Windows

## 📌 Visão Geral
Este sistema fornece uma interface gráfica para executar operações comuns de manutenção no Windows, como limpeza de arquivos temporários, reparos do sistema e otimização de disco, agrupando comandos técnicos em um painel acessível.

## 🛠️ Funcionalidades Principais

### 🔄 Operações de Limpeza
- **Limpeza de arquivos temporários** (pastas TEMP)
- **Limpeza de disco** (via `cleanmgr`)
- **Otimização de espaço** (remocão de arquivos obsoletos)

### 🛠️ Ferramentas de Reparo
- **Verificação de integridade** (SFC)
- **Reparo de imagem do sistema** (DISM)
- **Verificação de disco** (CHKDSK)

### ⚙️ Otimização do Sistema
- **Desfragmentação de disco**
- **Reset de configurações de rede**
- **Liberação de espaço em disco**

## 💻 Tecnologias Utilizadas

### 📚 Bibliotecas Python
| Biblioteca | Finalidade | Versão |
|------------|------------|--------|
| `os` | Operações no sistema de arquivos | Built-in |
| `subprocess` | Execução de comandos CMD | Built-in |
| `ctypes` | Interação com DLLs do Windows | Built-in |
| `tkinter` | Interface gráfica básica | Built-in |
| `shutil` | Operações avançadas com arquivos | Built-in |

### 🖥️ Dependências do Sistema
- Windows 7 ou superior
- Python 3.6+
- Acesso administrativo (para funções avançadas)

## ⚠️ Requisitos de Execução

1. **Privilégios de Administrador**:
   - Funções marcadas com ⚠️ requerem elevação
   - O sistema solicita UAC automaticamente

2. **Instalação Simples**:
   ```bash
   # Nenhuma instalação necessária além do Python padrão
   python manutencao.py

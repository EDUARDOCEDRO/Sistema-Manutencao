import os
import subprocess
import ctypes
import shutil
import sys
import customtkinter as ctk
from tkinter import messagebox

def run_as_admin():
    
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            return True
        
        
        hwnd = None
        operation = "runas" 
        executable = sys.executable
        params = " ".join([f'"{x}"' for x in sys.argv])
        

        result = ctypes.windll.shell32.ShellExecuteW(
            hwnd, operation, executable, params, None, 1
        )
        

        if result > 32:
            sys.exit(0)  
        return False
    except Exception as e:
        print(f"Erro na elevação: {e}")
        return False

class MaintenanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ferramentas de Manutenção do Windows")
        self.geometry("550x550")
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        
        self.create_widgets()
        self.check_admin_status()
    
    def check_admin_status(self):
        
        if not ctypes.windll.shell32.IsUserAnAdmin():
            self.admin_status = ctk.CTkLabel(
                self.main_frame,
                text="⚠️ Modo limitado (execute como administrador para todas as funções)",
                text_color="orange"
            )
            self.admin_status.pack(pady=5)
    
    def create_widgets(self):
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        title = ctk.CTkLabel(
            self.main_frame,
            text="🛠️ Manutenção do Windows",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(10, 5))
        
        subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Ferramentas de sistema para otimização e reparos",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 15))
        
        
        tools = [
            ("🗑️ Limpar Arquivos Temporários", self.clean_temp, False),
            ("🧹 Limpeza de Disco Completa", self.clean_disk, True),
            ("🔧 Reparar Arquivos do Sistema", self.repair_system, True),
            ("📀 Verificar e Reparar Disco", self.check_disk, True),
            ("⚡ Desfragmentar Unidades", self.defrag_disk, True),
            ("💾 Otimizar Espaço em Disco", self.free_space, True),
            ("🌐 Resetar Configurações de Rede", self.reset_network, True),
            ("📊 Visualizar Informações do Sistema", self.system_info, False),
            ("🚪 Sair do Programa", self.quit_app, False)
        ]
        
        for text, command, needs_admin in tools:
            btn = ctk.CTkButton(
                self.main_frame,
                text=text,
                command=lambda c=command, na=needs_admin: self.run_with_admin_check(c, na),
                height=40,
                corner_radius=6,
                font=("Arial", 12),
                anchor="w"
            )
            btn.pack(pady=4, padx=5, fill="x")
    
    def run_with_admin_check(self, command, needs_admin):
        
        if needs_admin and not ctypes.windll.shell32.IsUserAnAdmin():
            if not run_as_admin():
                messagebox.showwarning(
                    "Privilégios Necessários",
                    "Esta função requer execução como administrador.\n"
                    "Por favor, clique em 'Sim' quando solicitado."
                )
                return
        command()
    
    def clean_temp(self):
        try:
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                os.path.join(os.environ.get('SystemRoot', ''), 'Temp'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
            ]
            
            cleaned_files = 0
            cleaned_size = 0
            
            for folder in temp_dirs:
                if os.path.exists(folder):
                    for item in os.listdir(folder):
                        path = os.path.join(folder, item)
                        try:
                            if os.path.isfile(path):
                                size = os.path.getsize(path)
                                os.remove(path)
                                cleaned_files += 1
                                cleaned_size += size
                            elif os.path.isdir(path):
                                shutil.rmtree(path)
                                cleaned_files += 1
                        except Exception as e:
                            print(f"Não foi possível limpar {path}: {e}")
            
            messagebox.showinfo(
                "Limpeza Concluída",
                f"✅ {cleaned_files} arquivos temporários removidos\n"
                f"💾 Espaço liberado: {cleaned_size/1024/1024:.2f} MB"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Falha na limpeza:\n{e}")
    
    def clean_disk(self):

        try:
            subprocess.run('cleanmgr /sagerun:1', shell=True, check=True)
            messagebox.showinfo(
                "Limpeza Iniciada",
                "🧹 A limpeza de disco foi iniciada.\n"
                "Isso pode levar alguns minutos para ser concluído."
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"❌ Falha na limpeza de disco:\n{e}")
    
    def repair_system(self):
        
        try:
            commands = [
                'DISM /Online /Cleanup-Image /RestoreHealth',
                'sfc /scannow'
            ]
            
            for cmd in commands:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    raise subprocess.CalledProcessError(
                        process.returncode, cmd, stdout, stderr
                    )
            
            messagebox.showinfo(
                "Reparo Concluído",
                "✅ Verificação de sistema finalizada.\n"
                "Reinicie o computador para completar os reparos."
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                "Erro no Reparo",
                f"❌ Falha ao reparar o sistema:\n{e.stderr or e.stdout}"
            )
    
    def check_disk(self):
    
        try:
            result = subprocess.run(
                'chkdsk /f /r',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                messagebox.showinfo(
                    "Verificação Agendada",
                    "✅ A verificação de disco foi agendada.\n"
                    "Será executada na próxima reinicialização."
                )
            else:
                messagebox.showwarning(
                    "Aviso",
                    f"⚠️ O CHKDSK retornou um código inesperado:\n{result.stderr}"
                )
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Falha ao verificar disco:\n{e}")
    
    def defrag_disk(self):

        try:
            process = subprocess.Popen(
                'defrag C: /U /V',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            messagebox.showinfo(
                "Desfragmentação",
                "⚡ A desfragmentação foi iniciada em segundo plano.\n"
                "Este processo pode levar algum tempo para ser concluído."
            )
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Falha ao desfragmentar:\n{e}")
    
    def free_space(self):
    
        try:
            commands = [
                'vssadmin delete shadows /all /quiet',
                'dism /online /cleanup-image /startcomponentcleanup /resetbase'
            ]
            
            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)
            
            messagebox.showinfo(
                "Limpeza Concluída",
                "✅ Espaço em disco foi otimizado com sucesso."
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"❌ Falha ao liberar espaço:\n{e}")
    
    def reset_network(self):
    
        try:
            commands = [
                'netsh winsock reset',
                'netsh int ip reset',
                'ipconfig /release',
                'ipconfig /renew',
                'ipconfig /flushdns'
            ]
            
            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)
            
            messagebox.showinfo(
                "Rede Resetada",
                "✅ Configurações de rede foram redefinidas.\n"
                "Reinicie o computador para aplicar as alterações."
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"❌ Falha ao resetar rede:\n{e}")
    
    def system_info(self):
        
        try:
            info = subprocess.check_output(
                'systeminfo',
                shell=True,
                text=True,
                stderr=subprocess.STDOUT
            )[:2000]
            
            messagebox.showinfo(
                "Informações do Sistema",
                f"🖥️ Dados do sistema:\n\n{info}"
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"❌ Falha ao obter informações:\n{e.output}")
    
    def quit_app(self):
        
        self.destroy()
        sys.exit(0)

def main():

    if not ctypes.windll.shell32.IsUserAnAdmin():
        if not run_as_admin():
            ctypes.windll.user32.MessageBoxW(
                0,
                "Este aplicativo requer privilégios de administrador para todas as funções.\n"
                "Por favor, execute como administrador para acesso completo.",
                "Elevação Necessária",
                0x10 | 0x1 
            )
            sys.exit(1)
        else:
            sys.exit(0)
    

    app = MaintenanceApp()
    app.mainloop()

if __name__ == "__main__":
    main()
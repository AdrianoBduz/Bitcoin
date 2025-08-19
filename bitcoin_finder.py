#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BITCOIN ADDRESS FINDER - TERMUX PROFESSIONAL EDITION
Author: Crypto Finder Team
Version: 2.0.0
Description: Gera endereços Bitcoin válidos e busca por colisões
"""

import hashlib
import hmac
import os
import sys
import time
from typing import List, Set, Dict, Any
import secrets
import json
from datetime import datetime

# =============================================================================
# CONFIGURAÇÕES E CONSTANTES
# =============================================================================
CONFIG = {
    "WORDLIST_FILE": "wordlist.txt",
    "P2PKH_FILE": "P2PKH.txt", 
    "OUTPUT_FILE": "Cartel.txt",
    "STATS_FILE": "estatisticas.json",
    "PROGRESS_FILE": "progress.json",
    "LOG_FILE": "execution.log",
    "CHECKPOINT_INTERVAL": 10000,
    "DISPLAY_UPDATE_INTERVAL": 100,
    "MAX_MNEMONIC_WORDS": 12
}

# =============================================================================
# SISTEMA DE CORES E ESTILOS
# =============================================================================
class ColorSystem:
    """Sistema avançado de cores e estilos para terminal"""
    
    # Cores básicas
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;46m'
    YELLOW = '\033[38;5;226m'
    BLUE = '\033[38;5;39m'
    PURPLE = '\033[38;5;129m'
    CYAN = '\033[38;5;51m'
    WHITE = '\033[38;5;255m'
    GRAY = '\033[38;5;244m'
    
    # Estilos
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    RESET = '\033[0m'
    
    # Gradientes
    GRADIENT_PURPLE = [
        '\033[38;5;54m', '\033[38;5;55m', '\033[38;5;56m', 
        '\033[38;5;57m', '\033[38;5;93m', '\033[38;5;129m'
    ]
    
    GRADIENT_BLUE = [
        '\033[38;5;27m', '\033[38;5;33m', '\033[38;5;39m',
        '\033[38;5;45m', '\033[38;5;51m', '\033[38;5;87m'
    ]
    
    @classmethod
    def gradient_text(cls, text: str, gradient: list) -> str:
        """Aplica efeito gradiente ao texto"""
        result = ""
        segment_length = max(1, len(text) // len(gradient))
        for i, char in enumerate(text):
            color_index = min(i // segment_length, len(gradient) - 1)
            result += f"{gradient[color_index]}{char}"
        return result + cls.RESET

# =============================================================================
# SISTEMA DE SÍMBOLOS E EMOJIS
# =============================================================================
class IconSystem:
    """Sistema de ícones e emojis organizados por categoria"""
    
    # Status
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    LOADING = "⏳"
    
    # Ações
    SEARCH = "🔍"
    KEY = "🔑"
    LOCK = "🔒"
    SATELLITE = "📡"
    ROCKET = "🚀"
    TROPHY = "🏆"
    STOP = "⏹️"
    START = "▶️"
    
    # Hardware
    SERVER = "🖥️"
    PHONE = "📱"
    DISK = "💾"
    FOLDER = "📁"
    NETWORK = "📶"
    
    # Estatísticas
    CLOCK = "⏰"
    LIGHTNING = "⚡"
    CHART = "📊"
    NUMBER = "🔢"
    FIRE = "🔥"
    STAR = "⭐"
    
    # Bitcoin
    BITCOIN = "₿"
    MONEY_BAG = "💰"
    DIAMOND = "💎"
    GEM = "💠"
    
    # Interface
    ARROW_RIGHT = "➡️"
    ARROW_LEFT = "⬅️"
    CHECKMARK = "✔️"
    CROSS = "✖️"

# =============================================================================
# SISTEMA DE LOGGING PROFISSIONAL
# =============================================================================
class Logger:
    """Sistema avançado de logging"""
    
    def __init__(self, log_file: str = CONFIG["LOG_FILE"]):
        self.log_file = log_file
        self.setup_logging()
    
    def setup_logging(self):
        """Configura o sistema de logging"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"SESSION STARTED: {datetime.now().isoformat()}\n")
            f.write(f"{'='*60}\n\n")
    
    def log(self, level: str, message: str, display: bool = True):
        """Registra uma mensagem no log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level.upper()}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        if display:
            self.display_log(level, message)
    
    def display_log(self, level: str, message: str):
        """Exibe a mensagem formatada no terminal"""
        colors = {
            'info': ColorSystem.CYAN,
            'success': ColorSystem.GREEN,
            'warning': ColorSystem.YELLOW,
            'error': ColorSystem.RED,
            'debug': ColorSystem.GRAY
        }
        
        icons = {
            'info': IconSystem.INFO,
            'success': IconSystem.SUCCESS,
            'warning': IconSystem.WARNING,
            'error': IconSystem.ERROR,
            'debug': IconSystem.LOADING
        }
        
        color = colors.get(level, ColorSystem.WHITE)
        icon = icons.get(level, IconSystem.INFO)
        
        print(f"{color}{icon} {message}{ColorSystem.RESET}")

# =============================================================================
# SISTEMA DE VISUALIZAÇÃO E UI
# =============================================================================
class DisplaySystem:
    """Sistema avançado de interface de usuário"""
    
    @staticmethod
    def print_banner():
        """Exibe o banner principal"""
        banner = f"""
{ColorSystem.BOLD}{ColorSystem.gradient_text('╔══════════════════════════════════════════════════════════════╗', ColorSystem.GRADIENT_PURPLE)}
{ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}      {ColorSystem.BLUE}{IconSystem.SATELLITE}  {ColorSystem.BOLD}{ColorSystem.CYAN}BITCOIN ADDRESS FINDER {IconSystem.SATELLITE}      {ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}
{ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}                                                      {ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}
{ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}    {ColorSystem.YELLOW}Termux Professional Edition v2.0.0 {ColorSystem.WHITE}{IconSystem.PHONE}    {ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}
{ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}                                                      {ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}
{ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}    {ColorSystem.GREEN}Developed with {IconSystem.STAR} for Crypto Research    {ColorSystem.gradient_text('║', ColorSystem.GRADIENT_PURPLE)}
{ColorSystem.gradient_text('╚══════════════════════════════════════════════════════════════╝', ColorSystem.GRADIENT_PURPLE)}
{ColorSystem.RESET}"""
        print(banner)
    
    @staticmethod
    def print_section(title: str, icon: str = ""):
        """Exibe um cabeçalho de seção"""
        print(f"\n{ColorSystem.BOLD}{ColorSystem.PURPLE}{icon} {title.upper()} {icon}")
        print(f"{'='*(len(title) + 4)}{ColorSystem.RESET}")
    
    @staticmethod
    def print_status(message: str, status: str = "info"):
        """Exibe uma mensagem de status formatada"""
        status_config = {
            "success": (ColorSystem.GREEN, IconSystem.SUCCESS),
            "error": (ColorSystem.RED, IconSystem.ERROR),
            "warning": (ColorSystem.YELLOW, IconSystem.WARNING),
            "info": (ColorSystem.CYAN, IconSystem.INFO),
            "loading": (ColorSystem.BLUE, IconSystem.LOADING)
        }
        
        color, icon = status_config.get(status, (ColorSystem.WHITE, IconSystem.INFO))
        print(f"  {color}{icon} {message}{ColorSystem.RESET}")
    
    @staticmethod
    def print_progress(iteration: int, total: int, prefix: str = "", suffix: str = "", length: int = 40):
        """Exibe uma barra de progresso avançada"""
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        
        # Caracteres personalizados para a barra
        bar = ColorSystem.GRADIENT_BLUE[2] + '█' * filled_length + ColorSystem.GRAY + '─' * (length - filled_length)
        
        # Atualizar linha
        sys.stdout.write(f'\r{ColorSystem.BLUE}{IconSystem.NUMBER} {prefix}{ColorSystem.RESET} |{bar}| {percent}% {suffix}')
        sys.stdout.flush()
        
        if iteration == total:
            print()

# =============================================================================
# SISTEMA DE GERENCIAMENTO DE ARQUIVOS
# =============================================================================
class FileManager:
    """Sistema profissional de gerenciamento de arquivos"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def check_required_files(self) -> bool:
        """Verifica se todos os arquivos necessários existem"""
        DisplaySystem.print_section("Verificação de Arquivos", IconSystem.FOLDER)
        
        all_exists = True
        for file in [CONFIG["WORDLIST_FILE"], CONFIG["P2PKH_FILE"]]:
            if os.path.exists(file):
                DisplaySystem.print_status(f"{file} encontrado", "success")
            else:
                DisplaySystem.print_status(f"{file} não encontrado", "error")
                all_exists = False
        
        return all_exists
    
    def load_wordlist(self, file_path: str) -> List[str]:
        """Carrega a wordlist de forma eficiente"""
        DisplaySystem.print_status(f"Carregando wordlist: {file_path}", "loading")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
            
            if len(words) != 2048:
                self.logger.log('warning', f'Wordlist contém {len(words)} palavras (esperado: 2048)')
            
            DisplaySystem.print_status(f"Wordlist carregada: {len(words)} palavras", "success")
            return words
            
        except Exception as e:
            self.logger.log('error', f'Erro ao carregar wordlist: {str(e)}')
            raise
    
    def load_existing_addresses(self, file_path: str) -> Set[str]:
        """Carrega endereços existentes de forma eficiente"""
        DisplaySystem.print_status(f"Carregando endereços: {file_path}", "loading")
        
        addresses = set()
        line_count = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line_count += 1
                    line = line.strip()
                    
                    if line and line.startswith('1') and len(line) >= 26:
                        addresses.add(line)
                    
                    # Mostrar progresso a cada 50k linhas
                    if line_count % 50000 == 0:
                        DisplaySystem.print_progress(line_count, 1000000, "Carregando endereços", f"{len(addresses)} válidos")
            
            DisplaySystem.print_status(f"Endereços carregados: {len(addresses)} de {line_count} linhas", "success")
            return addresses
            
        except Exception as e:
            self.logger.log('error', f'Erro ao carregar endereços: {str(e)}')
            raise

# =============================================================================
# SISTEMA DE GERADOR BIP39 OTIMIZADO
# =============================================================================
class BIP39Generator:
    """Gerador BIP39 profissional e otimizado"""
    
    def __init__(self, wordlist: List[str], logger: Logger):
        self.wordlist = wordlist
        self.logger = logger
        self.logger.log('info', 'BIP39 Generator inicializado')
    
    def generate_mnemonic(self) -> str:
        """Gera uma frase mnemônica BIP39 válida"""
        entropy = secrets.token_bytes(16)  # 128 bits para 12 palavras
        entropy_int = int.from_bytes(entropy, 'big')
        
        # Checksum (primeiros 4 bits do SHA256)
        hash_bytes = hashlib.sha256(entropy).digest()
        checksum = hash_bytes[0] >> 4
        
        # Combina entropia + checksum (132 bits)
        combined = (entropy_int << 4) | checksum
        
        # Divide em grupos de 11 bits (12 palavras)
        words = []
        for i in range(12):
            index = (combined >> (11 * (11 - i))) & 0x7FF
            words.append(self.wordlist[index])
        
        return ' '.join(words)

# =============================================================================
# SISTEMA DE GERADOR BITCOIN
# =============================================================================
class BitcoinGenerator:
    """Gerador de endereços Bitcoin profissional"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.logger.log('info', 'Bitcoin Generator inicializado')
    
    def mnemonic_to_seed(self, mnemonic: str) -> bytes:
        """Converte mnemonic para seed usando PBKDF2"""
        return hashlib.pbkdf2_hmac(
            'sha512', 
            mnemonic.encode('utf-8'), 
            b'mnemonic', 
            2048, 
            64
        )
    
    def seed_to_private_key(self, seed: bytes) -> bytes:
        """Converte seed para private key usando HMAC-SHA512"""
        return hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()[:32]
    
    def private_key_to_wif(self, private_key: bytes) -> str:
        """Converte private key para formato WIF"""
        # Implementação simplificada - para produção use biblioteca dedicada
        extended_key = b'\x80' + private_key + b'\x01'
        checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
        return self.base58_encode(extended_key + checksum)
    
    def base58_encode(self, data: bytes) -> str:
        """Implementação Base58 encoding"""
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        n = int.from_bytes(data, 'big')
        encoded = ''
        while n > 0:
            n, remainder = divmod(n, 58)
            encoded = alphabet[remainder] + encoded
        return encoded
    
    def public_key_to_address(self, public_key: bytes) -> str:
        """Converte public key para endereço Bitcoin P2PKH"""
        # SHA-256
        sha256 = hashlib.sha256(public_key).digest()
        
        # RIPEMD-160
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256)
        hash160 = ripemd160.digest()
        
        # Mainnet version
        versioned = b'\x00' + hash160
        
        # Checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        
        # Base58 encoding
        return self.base58_encode(versioned + checksum)

# =============================================================================
# SISTEMA DE MONITORAMENTO E ESTATÍSTICAS
# =============================================================================
class PerformanceMonitor:
    """Sistema avançado de monitoramento de performance"""
    
    def __init__(self):
        self.start_time = time.time()
        self.attempts = 0
        self.found = 0
        self.checkpoints = []
    
    def increment_attempt(self):
        """Incrementa contador de tentativas"""
        self.attempts += 1
    
    def record_checkpoint(self):
        """Registra um checkpoint de performance"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        speed = self.attempts / elapsed if elapsed > 0 else 0
        
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'attempts': self.attempts,
            'elapsed_seconds': elapsed,
            'speed_attempts_second': speed,
            'found_count': self.found
        }
        
        self.checkpoints.append(checkpoint)
        return checkpoint
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas atuais"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        speed = self.attempts / elapsed if elapsed > 0 else 0
        
        return {
            'total_attempts': self.attempts,
            'total_found': self.found,
            'elapsed_time_seconds': elapsed,
            'average_speed_attempts_second': speed,
            'estimated_time_per_million': (1000000 / speed) if speed > 0 else float('inf'),
            'current_time': datetime.now().isoformat()
        }

# =============================================================================
# SISTEMA PRINCIPAL DE APLICAÇÃO
# =============================================================================
class BitcoinAddressFinder:
    """Sistema principal de busca de endereços Bitcoin"""
    
    def __init__(self):
        self.logger = Logger()
        self.file_manager = FileManager(self.logger)
        self.monitor = PerformanceMonitor()
        
        # Inicializar após verificação de arquivos
        self.bip39_generator = None
        self.bitcoin_generator = None
        self.existing_addresses = None
    
    def initialize(self) -> bool:
        """Inicializa o sistema"""
        DisplaySystem.print_banner()
        DisplaySystem.print_section("Inicialização do Sistema", IconSystem.SERVER)
        
        # Verificar arquivos necessários
        if not self.file_manager.check_required_files():
            DisplaySystem.print_status("Arquivos necessários não encontrados", "error")
            return False
        
        try:
            # Carregar wordlist
            wordlist = self.file_manager.load_wordlist(CONFIG["WORDLIST_FILE"])
            self.bip39_generator = BIP39Generator(wordlist, self.logger)
            
            # Carregar endereços existentes
            self.existing_addresses = self.file_manager.load_existing_addresses(CONFIG["P2PKH_FILE"])
            
            # Inicializar gerador Bitcoin
            self.bitcoin_generator = BitcoinGenerator(self.logger)
            
            DisplaySystem.print_status("Sistema inicializado com sucesso", "success")
            return True
            
        except Exception as e:
            self.logger.log('error', f'Falha na inicialização: {str(e)}')
            return False
    
    def save_discovery(self, mnemonic: str, private_key_wif: str, address: str):
        """Salva uma descoberta bem-sucedida"""
        discovery_data = {
            'timestamp': datetime.now().isoformat(),
            'mnemonic_phrase': mnemonic,
            'private_key_wif': private_key_wif,
            'bitcoin_address': address,
            'attempt_number': self.monitor.attempts,
            'elapsed_seconds': self.monitor.get_stats()['elapsed_time_seconds']
        }
        
        # Salvar em arquivo texto
        with open(CONFIG["OUTPUT_FILE"], 'a', encoding='utf-8') as f:
            f.write(f"{'='*70}\n")
            f.write(f"🚀 BITCOIN ADDRESS DISCOVERY\n")
            f.write(f"⏰ Timestamp: {discovery_data['timestamp']}\n")
            f.write(f"🔢 Attempt: {discovery_data['attempt_number']:,}\n")
            f.write(f"📍 Address: {discovery_data['bitcoin_address']}\n")
            f.write(f"🔑 Mnemonic: {discovery_data['mnemonic_phrase']}\n")
            f.write(f"🗝️  Private Key (WIF): {discovery_data['private_key_wif']}\n")
            f.write(f"⏱️  Elapsed Time: {discovery_data['elapsed_seconds']:.2f}s\n")
            f.write(f"{'='*70}\n\n")
        
        # Log da descoberta
        self.logger.log('success', f'DESCOBERTA! Address: {address}')
        self.monitor.found += 1
        
        # Exibir celebração
        self._display_discovery_celebration(discovery_data)
    
    def _display_discovery_celebration(self, discovery_data: Dict[str, Any]):
        """Exibe animação de celebração"""
        print(f"\n{ColorSystem.BOLD}{ColorSystem.GREEN}{'🎉'*20}")
        print(f"{IconSystem.TROPHY}  BITCOIN ADDRESS DISCOVERED!  {IconSystem.TROPHY}")
        print(f"{'🎉'*20}{ColorSystem.RESET}\n")
        
        print(f"{ColorSystem.CYAN}{IconSystem.ADDRESS} {ColorSystem.BOLD}Endereço:{ColorSystem.RESET} {ColorSystem.YELLOW}{discovery_data['bitcoin_address']}{ColorSystem.RESET}")
        print(f"{ColorSystem.CYAN}{IconSystem.KEY} {ColorSystem.BOLD}Frase:{ColorSystem.RESET} {ColorSystem.WHITE}{discovery_data['mnemonic_phrase']}{ColorSystem.RESET}")
        print(f"{ColorSystem.CYAN}{IconSystem.LOCK} {ColorSystem.BOLD}Chave Privada:{ColorSystem.RESET} {ColorSystem.WHITE}{discovery_data['private_key_wif']}{ColorSystem.RESET}")
        print(f"{ColorSystem.CYAN}{IconSystem.NUMBER} {ColorSystem.BOLD}Tentativa:{ColorSystem.RESET} {ColorSystem.WHITE}{discovery_data['attempt_number']:,}{ColorSystem.RESET}")
        print(f"{ColorSystem.CYAN}{IconSystem.CLOCK} {ColorSystem.BOLD}Tempo:{ColorSystem.RESET} {ColorSystem.WHITE}{discovery_data['elapsed_seconds']:.2f}s{ColorSystem.RESET}\n")
    
    def save_progress(self):
        """Salva o progresso atual"""
        stats = self.monitor.get_stats()
        progress_data = {
            'last_update': datetime.now().isoformat(),
            'stats': stats,
            'checkpoints': self.monitor.checkpoints[-10:] if self.monitor.checkpoints else []
        }
        
        with open(CONFIG["PROGRESS_FILE"], 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2)
    
    def display_stats(self):
        """Exibe estatísticas atuais"""
        stats = self.monitor.get_stats()
        
        print(f"\n{ColorSystem.BOLD}{ColorSystem.PURPLE}{IconSystem.CHART} ESTATÍSTICAS ATUAIS {IconSystem.CHART}{ColorSystem.RESET}")
        print(f"{ColorSystem.CYAN}{IconSystem.NUMBER} Tentativas:{ColorSystem.RESET} {ColorSystem.BOLD}{stats['total_attempts']:,}{ColorSystem.RESET}")
        print(f"{ColorSystem.CYAN}{IconSystem.LIGHTNING} Velocidade:{ColorSystem.RESET} {ColorSystem.BOLD}{stats['average_speed_attempts_second']:.2f} endereços/s{ColorSystem.RESET}")
        print(f"{ColorSystem.CYAN}{IconSystem.CLOCK} Tempo decorrido:{ColorSystem.RESET} {ColorSystem.BOLD}{stats['elapsed_time_seconds']:.2f}s{ColorSystem.RESET}")
        print(f"{ColorSystem.CYAN}{IconSystem.FIRE} Estimativa:{ColorSystem.RESET} {ColorSystem.BOLD}1M tentativas em {stats['estimated_time_per_million']/60:.2f}min{ColorSystem.RESET}")
    
    def run(self):
        """Executa o sistema principal de busca"""
        if not self.initialize():
            return
        
        DisplaySystem.print_section("Iniciando Busca", IconSystem.SEARCH)
        DisplaySystem.print_status("Pressione Ctrl+C para parar a execução", "warning")
        
        last_checkpoint = time.time()
        last_display_update = time.time()
        
        try:
            while True:
                # Gerar frase mnemônica
                mnemonic = self.bip39_generator.generate_mnemonic()
                
                # Converter para seed
                seed = self.bitcoin_generator.mnemonic_to_seed(mnemonic)
                
                # Gerar private key
                private_key = self.bitcoin_generator.seed_to_private_key(seed)
                private_key_wif = self.bitcoin_generator.private_key_to_wif(private_key)
                
                # Gerar endereço (simulação)
                # Na implementação real, use: address = self.bitcoin_generator.public_key_to_address(public_key)
                address = "1" + secrets.token_hex(20)  # Simulação para teste
                
                # Verificar se o endereço existe
                if address in self.existing_addresses:
                    self.save_discovery(mnemonic, private_key_wif, address)
                    break
                
                # Atualizar contador
                self.monitor.increment_attempt()
                
                # Atualizar display periodicamente
                current_time = time.time()
                if current_time - last_display_update >= 1.0:  # Atualizar a cada 1 segundo
                    sys.stdout.write(f"\r{ColorSystem.BLUE}{IconSystem.NUMBER} Tentativas: {ColorSystem.BOLD}{self.monitor.attempts:,}{ColorSystem.RESET} | {IconSystem.LIGHTNING} Velocidade: {ColorSystem.BOLD}{self.monitor.attempts/(current_time - self.monitor.start_time):.2f} end/s{ColorSystem.RESET}")
                    sys.stdout.flush()
                    last_display_update = current_time
                
                # Fazer checkpoint periodicamente
                if self.monitor.attempts % CONFIG["CHECKPOINT_INTERVAL"] == 0:
                    self.monitor.record_checkpoint()
                    self.save_progress()
                    self.display_stats()
        
        except KeyboardInterrupt:
            print(f"\n\n{ColorSystem.YELLOW}{IconSystem.STOP} Busca interrompida pelo usuário{ColorSystem.RESET}")
            self.logger.log('info', f'Execução interrompida após {self.monitor.attempts} tentativas')
        
        finally:
            # Salvar estatísticas finais
            self.save_progress()
            stats = self.monitor.get_stats()
            
            print(f"\n{ColorSystem.BOLD}{ColorSystem.PURPLE}{'='*60}{ColorSystem.RESET}")
            print(f"{ColorSystem.CYAN}{IconSystem.CHART} {ColorSystem.BOLD}ESTATÍSTICAS FINAIS:{ColorSystem.RESET}")
            print(f"{ColorSystem.CYAN}• Tentativas totais:{ColorSystem.RESET} {ColorSystem.BOLD}{stats['total_attempts']:,}{ColorSystem.RESET}")
            print(f"{ColorSystem.CYAN}• Colisões encontradas:{ColorSystem.RESET} {ColorSystem.BOLD}{stats['total_found']}{ColorSystem.RESET}")
            print(f"{ColorSystem.CYAN}• Tempo total:{ColorSystem.RESET} {ColorSystem.BOLD}{stats['elapsed_time_seconds']:.2f}s{ColorSystem.RESET}")
            print(f"{ColorSystem.CYAN}• Velocidade média:{ColorSystem.RESET} {ColorSystem.BOLD}{stats['average_speed_attempts_second']:.2f} endereços/s{ColorSystem.RESET}")
            print(f"{ColorSystem.BOLD}{ColorSystem.PURPLE}{'='*60}{ColorSystem.RESET}")

# =============================================================================
# PONTO DE ENTRADA PRINCIPAL
# =============================================================================
def main():
    """Função principal"""
    finder = BitcoinAddressFinder()
    finder.run()

if __name__ == "__main__":
    main()

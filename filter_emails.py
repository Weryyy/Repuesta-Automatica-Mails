#!/usr/bin/env python3
from src.utils.config import load_env_config
from src.agents.excel_writer_agent import ExcelWriterAgent
from src.agents.email_filter_agent import EmailFilterAgent
from src.agents.email_reader_agent import EmailReaderAgent
import sys
import os
from dotenv import load_dotenv

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def main():
    print("🚀 Iniciando proceso de filtrado de correos reales...")

    # Cargar configuración del .env
    config = load_env_config()

    if not config['email_address'] or not config['email_password']:
        print("❌ Error: No se encontraron credenciales en el archivo .env")
        return

    # 1. Configurar el lector de correos
    reader = EmailReaderAgent()
    reader.configure(
        email_address=config['email_address'],
        password=config['email_password'],
        imap_server=config['imap_server'],
        imap_port=config['imap_port']
    )

    print(
        f"📡 Conectando a {config['imap_server']} para {config['email_address']}...")
    if not reader.connect():
        print("❌ Error al conectar con el servidor de correo.")
        return

    # 2. Leer los últimos 50 correos
    print("📥 Descargando los últimos 50 correos para análisis global...")
    emails = reader.execute({'max_emails': 50})
    print(f"✅ Se han descargado {len(emails)} correos.")

    # 3. Configurar el filtro (vacío para ver TODO)
    filter_agent = EmailFilterAgent()
    filter_agent.configure({})

    print("🔍 Analizando todos los correos para métricas globales...")
    filtered_emails = filter_agent.execute(emails)
    print(f"🎯 Preparados {len(filtered_emails)} correos para el reporte.")

    # 4. Guardar resultados en Excel
    if filtered_emails:
        writer = ExcelWriterAgent()
        writer.configure(
            output_folder=config['output_folder'], filename="correos_filtrados.xlsx")

        print(
            f"📊 Guardando resultados en {config['output_folder']}/correos_filtrados.xlsx...")
        file_path = writer.execute(filtered_emails)
        print(
            f"✨ Proceso completado con éxito. Archivo creado en: {file_path}")
    else:
        print("ℹ️ No se encontraron correos para filtrar, no se creó el archivo Excel.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Demo script to test the email automation system without real email credentials.
This creates mock data to demonstrate the agent pipeline.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents import EmailFilterAgent, ExcelWriterAgent
from src.orchestrator import Orchestrator


def create_mock_emails():
    """Create mock email data for testing."""
    return [
        {
            'id': '1',
            'subject': 'Factura #12345',
            'from': 'ventas@empresa.com',
            'date': 'Mon, 10 Feb 2025 10:00:00',
            'body': 'Estimado cliente, adjuntamos la factura del mes...'
        },
        {
            'id': '2',
            'subject': 'Pedido confirmado',
            'from': 'pedidos@tienda.com',
            'date': 'Mon, 10 Feb 2025 11:30:00',
            'body': 'Su pedido ha sido confirmado y está en proceso...'
        },
        {
            'id': '3',
            'subject': 'Newsletter semanal',
            'from': 'newsletter@info.com',
            'date': 'Mon, 10 Feb 2025 12:00:00',
            'body': 'Las últimas noticias de esta semana...'
        },
        {
            'id': '4',
            'subject': 'Factura #12346',
            'from': 'ventas@empresa.com',
            'date': 'Mon, 10 Feb 2025 14:00:00',
            'body': 'Estimado cliente, adjuntamos otra factura...'
        },
        {
            'id': '5',
            'subject': 'Confirmación de registro',
            'from': 'soporte@servicio.com',
            'date': 'Mon, 10 Feb 2025 15:00:00',
            'body': 'Gracias por registrarte en nuestro servicio...'
        }
    ]


def demo_filter_and_export():
    """Demonstrate filtering and exporting emails to Excel."""
    print("=" * 60)
    print("🧪 DEMO - Sistema de Automatización de Correos")
    print("=" * 60)
    print("\n📧 Creando datos de correos de prueba...")
    
    # Create mock emails
    mock_emails = create_mock_emails()
    print(f"✅ Creados {len(mock_emails)} correos de prueba\n")
    
    # Show all emails
    print("📋 Lista de correos:")
    for email in mock_emails:
        print(f"  - {email['subject']} (De: {email['from']})")
    
    # Create and configure filter agent
    print("\n🔍 Configurando filtro para correos con 'Factura' en el asunto...")
    filter_agent = EmailFilterAgent()
    filter_agent.configure({
        'subject_contains': ['Factura']
    })
    
    # Create excel writer
    excel_writer = ExcelWriterAgent()
    excel_writer.configure(output_folder='output', filename='demo_emails.xlsx')
    
    # Create orchestrator
    orchestrator = Orchestrator("Demo Email to Excel")
    orchestrator.add_agent(filter_agent)
    orchestrator.add_agent(excel_writer)
    
    # Execute
    print("⚙️  Ejecutando orquestador...")
    result = orchestrator.execute(mock_emails)
    
    # Show results
    print("\n📊 Resultados de la ejecución:")
    print(f"Estado: {result['status']}")
    print(f"\nRegistro de ejecución:")
    for log in result['logs']:
        print(f"  Paso {log['step']}: {log['agent']} - {log['status']}")
    
    if result['status'] == 'completed':
        print(f"\n✅ Archivo Excel generado: {result['output']}")
        print("\n🎉 Demo completado exitosamente!")
    else:
        print(f"\n❌ Error: {result['status']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        demo_filter_and_export()
    except Exception as e:
        print(f"\n❌ Error durante el demo: {str(e)}")
        import traceback
        traceback.print_exc()

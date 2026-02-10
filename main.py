#!/usr/bin/env python3
"""
Main entry point for the Email Automation System.
Run this script to start the dashboard.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.dashboard import Dashboard


def main():
    """Start the dashboard application."""
    print("=" * 60)
    print("📧 Sistema de Automatización de Correos")
    print("=" * 60)
    print("\nIniciando el dashboard...")
    print("El dashboard se abrirá en tu navegador.")
    print("URL: http://localhost:5006")
    print("\nPresiona Ctrl+C para detener el servidor.")
    print("=" * 60)
    
    # Create and serve dashboard
    dashboard = Dashboard()
    dashboard.serve(port=5006, show=True)


if __name__ == "__main__":
    main()

import pandas as pd
import sys
import os

# Mock data
emails = [
    {'subject': 'Factura de luz', 'body': 'Su factura está lista'},
    {'subject': 'Confirmación de pedido', 'body': 'Gracias por su compra'},
    {'subject': 'Alerta de seguridad', 'body': 'Acceso detectado'},
    {'subject': 'Newsletter', 'body': 'Noticias de hoy'},
]

categories = {
    'Facturas/Pagos': ['factura', 'invoice', 'pago', 'bill', 'receipt', 'boleta'],
    'Pedidos/Compras': ['pedido', 'order', 'confirmación', 'purchase', 'shipping', 'envío'],
    'Seguridad': ['security', 'seguridad', 'password', 'login', 'alerta', 'alert', 'verify', 'google'],
    'Soporte/Ayuda': ['soporte', 'support', 'ayuda', 'ticket'],
}

counts = {cat: 0 for cat in categories}
counts['Otros'] = 0

for email_data in emails:
    subject = email_data.get('subject', '').lower()
    body = email_data.get('body', '').lower()
    text = f"{subject} {body}"
    
    found = False
    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            counts[cat] += 1
            found = True
            break
    
    if not found:
        counts['Otros'] += 1

print(counts)
df = pd.DataFrame([{'Tema': k, 'Cantidad': v} for k, v in counts.items() if v > 0])
print(df)

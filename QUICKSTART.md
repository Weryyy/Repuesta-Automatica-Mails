# 🚀 Guía de Inicio Rápido

## Instalación en 3 Pasos

### 1. Clonar e Instalar

```bash
git clone https://github.com/Weryyy/Repuesta-Automatica-Mails.git
cd Repuesta-Automatica-Mails
pip install -r requirements.txt
```

### 2. Probar con Demo (Opcional)

```bash
python demo.py
```

Este comando ejecutará un demo con datos ficticios y generará un archivo Excel de prueba.

### 3. Iniciar la Aplicación

```bash
python main.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:5006`

## Primer Uso

### Para Gmail

1. **Habilita IMAP en Gmail:**
   - Ve a Configuración → Ver toda la configuración
   - Pestaña "Reenvío y correo POP/IMAP"
   - Habilita "Activar IMAP"

2. **Crea una Contraseña de Aplicación:**
   - Ve a [myaccount.google.com](https://myaccount.google.com)
   - Seguridad → Verificación en dos pasos (actívala si no lo está)
   - Contraseñas de aplicaciones → Selecciona "Correo" y "Otro dispositivo"
   - Copia la contraseña generada (16 caracteres)

3. **En el Dashboard:**
   - Correo: `tu_email@gmail.com`
   - Contraseña: Pega la contraseña de aplicación (no tu contraseña normal)
   - Servidor IMAP: `imap.gmail.com` (ya configurado por defecto)

### Para Outlook/Hotmail

1. **Habilita IMAP:**
   - Ve a Configuración → Ver toda la configuración de Outlook
   - Correo → Sincronización de correo electrónico
   - Habilita IMAP

2. **En el Dashboard:**
   - Correo: `tu_email@outlook.com`
   - Contraseña: Tu contraseña normal
   - Servidor IMAP: `outlook.office365.com`

## Ejemplo de Uso: Exportar Facturas a Excel

### Paso 1: Configura el Escenario

En el dashboard:
- **Escenario:** Email a Excel
- **Correo:** tu_email@gmail.com
- **Contraseña:** [contraseña de aplicación]
- **Máximo de correos:** 20

### Paso 2: Configura Filtros

- **Filtrar por asunto:** factura, invoice
- **Filtrar por remitente:** ventas@empresa.com

### Paso 3: Ejecuta

Haz clic en "Ejecutar Escenario"

### Paso 4: Revisa Resultados

- El sistema mostrará el progreso en tiempo real
- Un archivo Excel se generará en la carpeta `output/`
- Ejemplo: `output/emails_20250210_153045.xlsx`

## Casos de Uso Comunes

### 1. Exportar Todos los Correos No Leídos

```
Máximo de correos: 50
Filtros: [dejar vacío]
```

### 2. Extraer Correos de un Cliente Específico

```
Máximo de correos: 100
Filtrar por remitente: cliente@empresa.com
```

### 3. Buscar Correos Importantes

```
Máximo de correos: 200
Filtrar por asunto: urgente, importante, crítico
```

### 4. Recopilar Notificaciones

```
Máximo de correos: 50
Filtrar por remitente: noreply@servicio.com
Filtrar por asunto: notificación
```

## Troubleshooting Rápido

### "Error de autenticación"
- **Gmail:** ¿Estás usando contraseña de aplicación?
- **Outlook:** ¿Está habilitado IMAP?
- Verifica que email y contraseña sean correctos

### "No module named 'panel'"
```bash
pip install -r requirements.txt
```

### "Puerto 5006 en uso"
Edita `main.py` y cambia:
```python
dashboard.serve(port=5007, show=True)
```

### "No se encontraron correos"
- Verifica que tienes correos en tu inbox
- Prueba aumentar "Máximo de correos"
- Prueba sin filtros primero

## Próximos Pasos

1. **Lee la documentación completa:** `DOCUMENTATION.md`
2. **Experimenta con diferentes filtros**
3. **Revisa el código para entender cómo funciona**
4. **Considera crear tus propios agentes y escenarios**

## Soporte

- **Issues:** [GitHub Issues](https://github.com/Weryyy/Repuesta-Automatica-Mails/issues)
- **Documentación:** `README.md` y `DOCUMENTATION.md`
- **Demo:** `python demo.py`

## Tips

💡 **Tip 1:** Empieza con pocos correos (10-20) para pruebas rápidas

💡 **Tip 2:** Usa filtros para encontrar exactamente lo que necesitas

💡 **Tip 3:** Los archivos Excel se guardan con timestamp, nunca se sobrescriben

💡 **Tip 4:** Puedes usar el demo.py para entender el flujo sin usar credenciales reales

💡 **Tip 5:** El dashboard muestra logs en tiempo real de cada paso

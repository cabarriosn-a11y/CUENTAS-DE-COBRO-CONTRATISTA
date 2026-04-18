# 🟢 Generador de Informes de Ejecución SENA

Aplicación web desarrollada en Python con **Streamlit** para automatizar la generación de las cuentas de cobro y los informes cualitativos de los instructores y contratistas del SENA.

## Características
- Generación automática de documentos Word basados en plantillas (`docxtpl`).
- Inserción dinámica de datos del contratista.
- Integración con IA (Google Gemini) para autodescribir evidencias fotográficas.

## Instalación en local
1. Clona este repositorio:
   `git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git`
2. Instala las dependencias:
   `pip install -r requirements.txt`
3. Agrega tus archivos Word base renombrados como:
   - `PLANTILLA_Cualitativo.docx`
   - `PLANTILLA_GCCON.docx`
4. Ejecuta la aplicación:
   `streamlit run app.py`

## Notas
Las plantillas de Word deben contener las etiquetas en formato `{{ nombre_etiqueta }}` para que la aplicación pueda reemplazarlas correctamente.
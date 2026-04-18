import streamlit as st
from PIL import Image
import io
import os
import google.generativeai as genai
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Configuración de página
st.set_page_config(page_title="SENA Docs | Autodescripción", page_icon="🟢", layout="centered")

# --- CONFIGURACIÓN DE LA IA (Gemini) ---
# En GitHub, las claves se manejan con "st.secrets"
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    modelo = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("⚠️ Clave de API de Gemini no configurada. La IA operará en modo simulación.")

def analizar_imagen(imagen_bytes, competencia, ficha):
    try:
        # Aquí enviaríamos la imagen a la IA
        # prompt = f"Eres instructor SENA. Describe esta foto de la ficha {ficha} en la competencia {competencia} en máximo 2 líneas."
        # respuesta = modelo.generate_content([prompt, imagen_bytes])
        # return respuesta.text
        return f"Instructor orientando la competencia '{competencia}' a los aprendices de la ficha {ficha}."
    except Exception as e:
        return f"Error en IA: {str(e)}"

st.title("🟢 Generador de Informes SENA")
st.markdown("Automatiza tu GCCON-F-087 y el Informe Cualitativo")

# Formularios de Entrada
col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre Completo")
    ficha = st.text_input("Número de Ficha")
    mes = st.selectbox("Mes de Cobro", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"])
with col2:
    cedula = st.text_input("Cédula")
    competencia = st.text_input("Competencia")
    contrato = st.text_input("Número de Contrato")

st.divider()

# Carga de Evidencia
foto_subida = st.file_uploader("Sube una evidencia fotográfica", type=["jpg", "png"])

if foto_subida:
    imagen = Image.open(foto_subida)
    st.image(imagen, caption="Evidencia", use_column_width=True)
    
    if st.button("✨ Generar Descripción IA"):
        with st.spinner("Analizando con Inteligencia Artificial..."):
            descripcion = analizar_imagen(foto_subida.getvalue(), competencia, ficha)
            st.session_state['descripcion_ia'] = descripcion
            
    if 'descripcion_ia' in st.session_state:
        desc_final = st.text_area("Edita la descripción si lo necesitas:", st.session_state['descripcion_ia'])
        
        if st.button("📄 Generar Word"):
            try:
                # Lógica para inyectar datos en la plantilla Word
                # Requiere que exista el archivo 'PLANTILLA_Cualitativo.docx' en la misma carpeta
                doc = DocxTemplate("PLANTILLA_Cualitativo.docx")
                
                # Preparamos la imagen para el Word
                img_stream = io.BytesIO(foto_subida.getvalue())
                imagen_word = InlineImage(doc, img_stream, width=Mm(120))
                
                contexto = {
                    'nombre_contratista': nombre,
                    'cedula': cedula,
                    'mes_reporte': mes,
                    'numero_contrato': contrato,
                    'foto_1': imagen_word,
                    'descripcion_foto_1': desc_final
                }
                
                doc.render(contexto)
                
                # Guardar en memoria para descarga directa
                bio = io.BytesIO()
                doc.save(bio)
                
                st.download_button(
                    label="⬇️ Descargar Informe Listo",
                    data=bio.getvalue(),
                    file_name=f"Informe_Cualitativo_{cedula}_{mes}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                st.success("¡Documento generado con éxito!")
            except Exception as e:
                st.error(f"Error al generar el Word. ¿Aseguraste poner el archivo 'PLANTILLA_Cualitativo.docx' en la carpeta? Detalle: {e}")
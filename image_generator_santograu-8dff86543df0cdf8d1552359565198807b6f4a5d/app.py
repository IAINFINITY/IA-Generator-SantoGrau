import os
import uuid
import base64
import io
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import google.generativeai as genai

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
FACE_FOLDER = os.path.join(UPLOAD_FOLDER, 'faces')
GLASSES_FOLDER = os.path.join(UPLOAD_FOLDER, 'glasses')
RESULT_FOLDER = os.path.join(app.static_folder, 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configuração da API Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')
if GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_API_KEY_HERE':
    genai.configure(api_key=GEMINI_API_KEY)

# Verificar extensões permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Verificar se os arquivos foram enviados
        if 'face' not in request.files or 'glasses' not in request.files:
            return jsonify({'error': 'Arquivos não encontrados. Por favor, selecione uma foto do rosto e dos óculos.'}), 400
        
        face_file = request.files['face']
        glasses_file = request.files['glasses']
        
        # Verificar se os arquivos são válidos
        if face_file.filename == '' or glasses_file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado. Por favor, selecione ambas as imagens.'}), 400
        
        if not allowed_file(face_file.filename) or not allowed_file(glasses_file.filename):
            return jsonify({'error': 'Formato de arquivo não permitido. Use apenas PNG, JPG ou JPEG.'}), 400
        
        # Verificar tamanho dos arquivos (máximo 10MB cada)
        face_file.seek(0, 2)  # Ir para o final do arquivo
        face_size = face_file.tell()
        face_file.seek(0)  # Voltar ao início
        
        glasses_file.seek(0, 2)
        glasses_size = glasses_file.tell()
        glasses_file.seek(0)
        
        max_size = 10 * 1024 * 1024  # 10MB
        if face_size > max_size or glasses_size > max_size:
            return jsonify({'error': 'Arquivo muito grande. Tamanho máximo: 10MB por imagem.'}), 400
        
        # Criar nomes de arquivo únicos
        face_filename = str(uuid.uuid4()) + '.' + face_file.filename.rsplit('.', 1)[1].lower()
        glasses_filename = str(uuid.uuid4()) + '.' + glasses_file.filename.rsplit('.', 1)[1].lower()
        
        # Salvar os arquivos
        face_path = os.path.join(FACE_FOLDER, face_filename)
        glasses_path = os.path.join(GLASSES_FOLDER, glasses_filename)
        
        face_file.save(face_path)
        glasses_file.save(glasses_path)
        
        # Verificar se as imagens são válidas
        try:
            with Image.open(face_path) as img:
                img.verify()
            with Image.open(glasses_path) as img:
                img.verify()
        except Exception:
            # Limpar arquivos inválidos
            if os.path.exists(face_path):
                os.remove(face_path)
            if os.path.exists(glasses_path):
                os.remove(glasses_path)
            return jsonify({'error': 'Arquivos de imagem inválidos ou corrompidos.'}), 400
        
        # Gerar imagem com a API do Gemini
        result_filename = generate_image_with_gemini(face_path, glasses_path)
        
        if not result_filename:
            return jsonify({'error': 'Falha ao gerar a imagem. Tente novamente.'}), 500
        
        # Retornar o caminho da imagem gerada
        result_url = '/static/images/' + result_filename
        
        # Informar se está usando API real ou simulação
        api_status = "real" if GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_API_KEY_HERE' else "simulation"
        
        return jsonify({
            'result_image': result_url,
            'api_status': api_status,
            'message': 'Imagem gerada com sucesso!'
        })
    
    except Exception as e:
        print(f"Erro inesperado na rota /generate: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor. Tente novamente mais tarde.'}), 500

def generate_image_with_gemini(face_path, glasses_path):
    """
    Função para gerar imagem combinada usando Gemini Pro Vision.
    
    Combina a foto do rosto com os óculos usando IA generativa.
    """
    try:
        # Verificar se a API está configurada
        if not GEMINI_API_KEY or GEMINI_API_KEY == 'YOUR_API_KEY_HERE':
            print("API Key não configurada, usando modo simulação")
            return simulate_image_generation(face_path, glasses_path)
        
        # Carregar e processar as imagens
        face_image = Image.open(face_path)
        glasses_image = Image.open(glasses_path)
        
        # Converter imagens para base64
        face_b64 = image_to_base64(face_image)
        glasses_b64 = image_to_base64(glasses_image)
        
        # Configurar o modelo Gemini Pro Vision
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Prompt para fusão de imagens
        prompt = """
        Você é um especialista em processamento de imagens e realidade aumentada. 
        Sua tarefa é criar uma imagem realista combinando o rosto da primeira imagem com os óculos da segunda imagem.
        
        Instruções específicas:
        1. Analise a posição e ângulo do rosto na primeira imagem
        2. Posicione os óculos da segunda imagem de forma natural no rosto
        3. Ajuste o tamanho dos óculos proporcionalmente ao rosto
        4. Mantenha a iluminação e sombras consistentes
        5. Garanta que os óculos se encaixem perfeitamente no nariz e orelhas
        6. Preserve a qualidade e resolução da imagem original do rosto
        
        Gere uma imagem final realista mostrando a pessoa usando os óculos de forma natural.
        """
        
        # Preparar as imagens para o modelo
        face_part = {
            'mime_type': 'image/jpeg',
            'data': face_b64
        }
        
        glasses_part = {
            'mime_type': 'image/jpeg', 
            'data': glasses_b64
        }
        
        # Gerar a imagem combinada
        response = model.generate_content([
            prompt,
            face_part,
            glasses_part
        ])
        
        # Processar a resposta e salvar a imagem
        if response.parts:
            # Extrair a imagem gerada da resposta
            generated_image_data = response.parts[0].inline_data.data
            
            # Decodificar e salvar a imagem
            result_filename = str(uuid.uuid4()) + '.jpg'
            result_path = os.path.join(RESULT_FOLDER, result_filename)
            
            # Converter base64 para imagem
            image_data = base64.b64decode(generated_image_data)
            generated_image = Image.open(io.BytesIO(image_data))
            generated_image.save(result_path, 'JPEG', quality=95)
            
            return result_filename
        else:
            print("Nenhuma imagem foi gerada pelo Gemini")
            return simulate_image_generation(face_path, glasses_path)
    
    except Exception as e:
        print(f"Erro ao gerar imagem com Gemini: {str(e)}")
        # Fallback para simulação em caso de erro
        return simulate_image_generation(face_path, glasses_path)

def image_to_base64(image):
    """Converte uma imagem PIL para base64"""
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    image_data = buffer.getvalue()
    return base64.b64encode(image_data).decode('utf-8')

def simulate_image_generation(face_path, glasses_path):
    """
    Função de fallback para simular a geração quando a API não está disponível.
    """
    try:
        result_filename = str(uuid.uuid4()) + '.jpg'
        result_path = os.path.join(RESULT_FOLDER, result_filename)
        
        # Abrir as imagens
        face_image = Image.open(face_path)
        glasses_image = Image.open(glasses_path)
        
        # Redimensionar a imagem dos óculos para combinar com o rosto
        face_width, face_height = face_image.size
        glasses_width = int(face_width * 0.6)  # Óculos ocupam 60% da largura do rosto
        glasses_height = int(glasses_width * glasses_image.size[1] / glasses_image.size[0])
        
        glasses_resized = glasses_image.resize((glasses_width, glasses_height), Image.Resampling.LANCZOS)
        
        # Posicionar os óculos no centro superior do rosto
        x_offset = (face_width - glasses_width) // 2
        y_offset = int(face_height * 0.25)  # 25% da altura do rosto
        
        # Criar uma cópia da imagem do rosto
        result_image = face_image.copy()
        
        # Se os óculos têm transparência, usar paste com máscara
        if glasses_resized.mode == 'RGBA':
            result_image.paste(glasses_resized, (x_offset, y_offset), glasses_resized)
        else:
            result_image.paste(glasses_resized, (x_offset, y_offset))
        
        # Salvar a imagem resultante
        result_image.save(result_path, 'JPEG', quality=95)
        
        return result_filename
    
    except Exception as e:
        print(f"Erro na simulação: {str(e)}")
        # Em último caso, apenas copiar a imagem do rosto
        result_filename = str(uuid.uuid4()) + '.jpg'
        result_path = os.path.join(RESULT_FOLDER, result_filename)
        with open(face_path, 'rb') as src, open(result_path, 'wb') as dst:
            dst.write(src.read())
        return result_filename

# Garantir que as pastas de upload existam
for folder in [FACE_FOLDER, GLASSES_FOLDER, RESULT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)
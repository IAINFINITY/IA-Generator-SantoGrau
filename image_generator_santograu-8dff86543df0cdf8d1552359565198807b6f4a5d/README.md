# 👓 Santo Grau - Experimente Óculos Virtualmente

![Santo Grau Logo](static/images/glasses-icon.svg)

## 📋 Sobre o Projeto

O **Santo Grau** é uma aplicação web inovadora que permite aos usuários experimentar óculos virtualmente através de inteligência artificial. Com uma interface moderna e intuitiva, os usuários podem fazer upload de uma foto do rosto e uma foto dos óculos para visualizar como ficariam usando o produto.

### 🎯 Funcionalidades Principais

- 📸 **Upload de Imagens**: Interface amigável para upload de fotos do rosto e óculos
- 🔍 **Preview em Tempo Real**: Visualização das imagens antes do processamento
- 🤖 **Processamento com IA**: Integração preparada para API do Google Gemini
- 💾 **Download de Resultados**: Baixe a imagem gerada diretamente
- 📱 **Compartilhamento**: Compartilhe seus resultados nas redes sociais
- 🎨 **Design Responsivo**: Interface adaptável para diferentes dispositivos

## 🚀 Demonstração

### Interface Principal
A aplicação possui uma interface limpa e moderna com as cores da marca Santo Grau:

- **Cores Principais**: Roxo (#4b2c7d) e Amarelo Dourado (#f7c600)
- **Design**: Minimalista e focado na experiência do usuário
- **Responsividade**: Funciona perfeitamente em desktop e mobile

### Fluxo de Uso
1. Faça upload de uma foto frontal do seu rosto
2. Faça upload de uma foto dos óculos desejados
3. Clique em "Gerar Visualização"
4. Visualize o resultado e baixe ou compartilhe

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Flask 2.3.3** - Framework web minimalista
- **Werkzeug 2.3.7** - Utilitários WSGI
- **Pillow 10.0.0** - Processamento de imagens
- **Google Generative AI 0.3.1** - API do Gemini (preparado)

### Frontend
- **HTML5** - Estrutura semântica
- **CSS3** - Estilos modernos com variáveis CSS
- **JavaScript ES6+** - Interatividade e AJAX
- **Google Fonts** - Tipografia Montserrat

### Recursos Adicionais
- **UUID** - Geração de nomes únicos para arquivos
- **FileReader API** - Preview de imagens no cliente
- **Fetch API** - Comunicação assíncrona com o servidor
- **Web Share API** - Compartilhamento nativo

## 📁 Estrutura do Projeto

```
santo-grau/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── README.md             # Documentação do projeto
├── .gitattributes        # Configurações Git
├── templates/
│   └── index.html        # Template principal da aplicação
├── static/
│   ├── css/
│   │   └── style.css     # Estilos da aplicação
│   ├── js/
│   │   └── script.js     # JavaScript da aplicação
│   ├── images/           # Imagens geradas e ícones
│   │   ├── face-icon.svg
│   │   └── glasses-icon.svg
│   └── uploads/          # Diretório para uploads
│       ├── faces/        # Fotos de rostos
│       └── glasses/      # Fotos de óculos
└── __pycache__/          # Cache Python (ignorado no Git)
```

## ⚙️ Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/santo-grau.git
   cd santo-grau
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure a API do Gemini**
   
   **Opção 1: Usando arquivo .env (Recomendado)**
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   
   # Edite o arquivo .env e adicione sua chave API
   GEMINI_API_KEY=sua_chave_api_real_aqui
   ```
   
   **Opção 2: Variável de ambiente**
   ```bash
   # Windows
   set GEMINI_API_KEY=sua_chave_api_aqui
   
   # Linux/Mac
   export GEMINI_API_KEY=sua_chave_api_aqui
   ```

5. **Execute a aplicação**
   ```bash
   python app.py
   ```

6. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## 🔧 Configuração da API

### Google Gemini API

A aplicação agora está **totalmente integrada** com o Google Gemini Pro Vision para processamento real de imagens!

#### Como obter sua chave API:

1. **Acesse o Google AI Studio**
   - Visite: https://makersuite.google.com/app/apikey
   - Faça login com sua conta Google

2. **Crie uma nova chave API**
   - Clique em "Create API Key"
   - Selecione um projeto ou crie um novo
   - Copie a chave gerada

3. **Configure a chave na aplicação**
   ```bash
   # Método 1: Arquivo .env (Mais seguro)
   cp .env.example .env
   # Edite o arquivo .env e substitua:
   GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   
   # Método 2: Variável de ambiente
   export GEMINI_API_KEY="AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

#### Funcionalidades da Integração:

- ✅ **Fusão Real de Imagens**: Combina rosto + óculos usando IA
- ✅ **Processamento Inteligente**: Ajusta posição, tamanho e perspectiva
- ✅ **Qualidade Profissional**: Resultados realistas e naturais
- ✅ **Fallback Automático**: Funciona em modo simulação sem API
- ✅ **Tratamento de Erros**: Mensagens claras para o usuário

#### Limitações e Considerações:

- **Tamanho máximo**: 10MB por imagem
- **Formatos suportados**: JPG, JPEG, PNG, GIF
- **Qualidade da foto**: Fotos frontais e bem iluminadas funcionam melhor
- **Custo**: Consulte os preços da API do Google Gemini

## 📝 Como Usar

### Upload de Imagens
1. **Foto do Rosto**: Faça upload de uma foto frontal, bem iluminada
2. **Foto dos Óculos**: Faça upload de uma foto clara dos óculos

### Formatos Suportados
- PNG
- JPG/JPEG

### Requisitos das Imagens
- **Rosto**: Foto frontal, boa iluminação, rosto claramente visível
- **Óculos**: Foto clara, preferencialmente com fundo neutro

## 🎨 Personalização

### Cores da Marca
As cores podem ser facilmente alteradas no arquivo `static/css/style.css`:

```css
:root {
    --primary-color: #4b2c7d;    /* Roxo Santo Grau */
    --secondary-color: #6a3da3;  /* Roxo mais claro */
    --accent-color: #f7c600;     /* Amarelo dourado */
}
```

### Layout e Componentes
- Modifique `templates/index.html` para alterações estruturais
- Ajuste `static/css/style.css` para mudanças visuais
- Customize `static/js/script.js` para novas funcionalidades

## 🚀 Deploy

### Heroku
```bash
# Instalar Heroku CLI
# Criar Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create santo-grau-app
git push heroku main
```

### Vercel
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição
- Mantenha o código limpo e bem documentado
- Siga as convenções de nomenclatura existentes
- Teste suas alterações antes de submeter
- Atualize a documentação quando necessário

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Equipe

- **Desenvolvedor Principal**: [Seu Nome]
- **Design**: Equipe Santo Grau
- **Consultoria IA**: [Nome do Consultor]

## 📞 Contato

- **Website**: [https://santograu.com.br](https://santograu.com.br)
- **Email**: contato@santograu.com.br
- **LinkedIn**: [Santo Grau](https://linkedin.com/company/santograu)

## 🙏 Agradecimentos

- Google AI pela API Gemini
- Comunidade Flask pelo framework
- Contribuidores open source
- Equipe Santo Grau pelo design e conceito

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no GitHub!**

![Santo Grau](https://img.shields.io/badge/Santo%20Grau-Experimente%20%C3%93culos%20Virtualmente-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=for-the-badge&logo=flask)
![AI](https://img.shields.io/badge/AI-Gemini%20Ready-orange?style=for-the-badge&logo=google)
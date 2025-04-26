# 🎓 Proyecto de Grado  
**Daniel Alejandro Romero Moreno**  
**Ingeniería de Software — Universidad de Santander (UDES)**  
📅 Diciembre 2024

---

## 🌍 Descripción General  
**Liquid Strength Sensor** es un sistema IoT + IA que mide la humedad de mezclas de concreto en tiempo real y predice su resistencia estructural utilizando Machine Learning, contribuyendo a construcciones más seguras y eficientes.

Componentes principales:  
- Hardware de bajo costo (ESP32 + Sensor Capacitivo)  
- Backend en Django para recepción y procesamiento de datos  
- Dashboard web moderno para visualizar métricas clave

**🎯 Objetivo:** Mejorar la calidad de estructuras mediante control continuo del proceso de fraguado.

---

## ⚙️ Tecnologías Utilizadas

### Hardware
- **ESP32 WROOM-32D**  
- **Sensor capacitivo de humedad**  
- **PCB personalizada** (EasyEDA)

### Firmware
- **MicroPython**  
- **Comunicación HTTP REST**

### Backend
- **Django 4.2**  
- **Django REST Framework**  
- **Django AllAuth**

### Frontend
- **Tailwind CSS**  
- **HTML5**  
- **JavaScript**

### Machine Learning
- **TensorFlow**  
- **scikit-learn**

### Base de Datos
- **SQLite3** (desarrollo)

### DevOps
- **Git, GitHub**  

---

## 🚀 Instalación Rápida

```bash
# 1. Clona este repositorio
git clone https://github.com/Daniromero1410/Liquid.git
cd Liquid

# 2. Crea y activa un entorno virtual
python -m venv venv
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Realiza migraciones de base de datos
python manage.py migrate

# 5. Crea un superusuario
python manage.py createsuperuser

# 6. Corre el servidor de desarrollo
python manage.py runserver

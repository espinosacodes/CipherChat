# 🌐 Guía de Comunicación Entre Máquinas - CipherChat

Esta guía te muestra cómo usar CipherChat para comunicación segura entre dos o más máquinas diferentes.

## 🔄 **Método 1: Transferencia Manual de Archivos (Recomendado)**

### Ventajas:
- ✅ **Más seguro** - No requiere conexión de red
- ✅ **Simple** - Fácil de implementar
- ✅ **Compatible** - Funciona con cualquier método de transferencia
- ✅ **Offline** - No depende de internet

### Proceso Paso a Paso:

#### 📱 **Máquina A (Alice)**

1. **Instalar CipherChat:**
   ```bash
   git clone <repository>
   cd CipherChat
   python setup.py
   ```

2. **Activar entorno y ejecutar:**
   ```bash
   source cipherchat_env/bin/activate  # Linux/Mac
   # o cipherchat_env\Scripts\activate  # Windows
   python cipherchat.py
   ```

3. **Crear usuario:**
   - Opción 1 (User Management) → 1 (Create New User) → "alice"
   - Opción 1 → 2 (Select User) → alice

4. **Exportar clave pública:**
   - Opción 2 (Key Management) → 1 (Export My Public Key)
   - Guardar como: `alice_public.pem`

5. **Crear mensaje de intercambio:**
   - Opción 5 (Key Exchange) → 1 (Send my public key)
   - Recipient: bob
   - Se genera: `key_exchange_alice_to_bob.json`

6. **Transferir a Máquina B:**
   - `alice_public.pem`
   - `key_exchange_alice_to_bob.json`

#### 📱 **Máquina B (Bob)**

1. **Instalar CipherChat** (igual que Máquina A)

2. **Crear usuario "bob"** y seleccionarlo

3. **Importar clave de Alice:**
   - Opción 2 → 2 (Import Someone's Public Key)
   - Username: alice
   - File: `alice_public.pem`

4. **Procesar intercambio de claves:**
   - Opción 5 → 2 (Process received key exchange)
   - File: `key_exchange_alice_to_bob.json`

5. **Crear respuesta de intercambio:**
   - Opción 5 → 1 (Send my public key)
   - Recipient: alice
   - Se genera: `key_exchange_bob_to_alice.json`

6. **Exportar clave pública:**
   - Opción 2 → 1 (Export My Public Key)
   - Guardar como: `bob_public.pem`

7. **Transferir a Máquina A:**
   - `bob_public.pem`
   - `key_exchange_bob_to_alice.json`

#### 🔄 **Finalizar en Máquina A**

1. **Importar clave de Bob:**
   - Opción 2 → 2 (Import Someone's Public Key)
   - Username: bob
   - File: `bob_public.pem`

2. **Procesar intercambio de Bob:**
   - Opción 5 → 2 (Process received key exchange)
   - File: `key_exchange_bob_to_alice.json`

#### 💬 **Enviar Mensajes**

**En cualquier máquina:**
1. Opción 3 (Send Message)
2. Recipient: [nombre del otro usuario]
3. Message: [tu mensaje secreto]
4. Se genera archivo: `[sender]_to_[recipient]_[timestamp].json`

**Para recibir:**
1. Transferir el archivo de mensaje a la máquina destinataria
2. Opción 4 (Receive Message)
3. Seleccionar archivo recibido
4. ¡Mensaje descifrado!

### 📁 **Métodos de Transferencia**

| Método | Seguridad | Velocidad | Facilidad |
|--------|-----------|-----------|-----------|
| **USB/Pendrive** | 🔒🔒🔒🔒🔒 | ⚡⚡⚡ | 👍👍👍👍 |
| **Email** | 🔒🔒🔒 | ⚡⚡⚡⚡ | 👍👍👍👍👍 |
| **Google Drive** | 🔒🔒🔒 | ⚡⚡⚡⚡ | 👍👍👍👍👍 |
| **WhatsApp/Telegram** | 🔒🔒🔒 | ⚡⚡⚡⚡⚡ | 👍👍👍👍👍 |
| **WeTransfer** | 🔒🔒 | ⚡⚡⚡⚡ | 👍👍👍👍 |
| **SSH/SCP** | 🔒🔒🔒🔒🔒 | ⚡⚡⚡⚡ | 👍👍 |

---

## 🌐 **Método 2: Servidor de Relay (Avanzado)**

### Ventajas:
- ✅ **Tiempo real** - Mensajes instantáneos
- ✅ **Automático** - Sin transferencia manual
- ✅ **Escalable** - Múltiples usuarios

### Desventajas:
- ❌ **Requiere servidor** - Necesita máquina intermedia
- ❌ **Conexión de red** - Dependiente de internet
- ❌ **Más complejo** - Configuración adicional

### Configuración:

#### 🖥️ **Máquina Servidor**

```bash
# En una máquina accesible desde internet
source cipherchat_env/bin/activate
python simple_server.py
```

#### 📱 **Clientes**

```bash
# En cada máquina cliente
source cipherchat_env/bin/activate
python simple_server.py client
```

---

## 🧪 **Método 3: Simulación Local**

Para probar antes de usar máquinas reales:

```bash
source cipherchat_env/bin/activate
python network_demo.py
```

Esto simula dos máquinas en tu computadora y te muestra exactamente qué archivos se intercambian.

---

## 🔐 **Consideraciones de Seguridad**

### ✅ **Ventajas del Diseño CipherChat**

1. **Cifrado Híbrido:** RSA + AES para máxima seguridad
2. **Claves Privadas Seguras:** Nunca salen de la máquina
3. **Firmas Digitales:** Detectan manipulación
4. **Forward Secrecy:** Cada mensaje usa clave AES única

### 🛡️ **Recomendaciones**

1. **Transferencia Segura:**
   - Usa métodos confiables para transferir archivos
   - Verifica integridad de archivos recibidos

2. **Almacenamiento:**
   - Mantén claves privadas seguras
   - Borra archivos temporales después del uso

3. **Verificación:**
   - Confirma identidad por canal secundario
   - Verifica firmas digitales

4. **Backups:**
   - Respalda claves privadas de forma segura
   - No pierdas acceso a tus claves

---

## 🚀 **Scripts de Automatización**

### 📤 **Script de Envío (send_to_machine.sh)**

```bash
#!/bin/bash
# Automatizar envío a otra máquina

echo "🔐 CipherChat - Envío Automático"
echo "Recipient: $1"
echo "Message: $2"

source cipherchat_env/bin/activate
python -c "
from src.key_manager import KeyManager
from src.secure_channel import SecureChannel
import sys

km = KeyManager()
sc = SecureChannel(km)
msg = sc.send_message('$USER', '$1', '$2')
if msg:
    with open('message_to_send.json', 'w') as f:
        f.write(sc.export_message_for_transmission(msg))
    print('✅ Mensaje guardado en: message_to_send.json')
"
```

### 📥 **Script de Recepción (receive_from_machine.sh)**

```bash
#!/bin/bash
# Automatizar recepción desde otra máquina

echo "🔐 CipherChat - Recepción Automática"
echo "File: $1"

source cipherchat_env/bin/activate
python -c "
from src.key_manager import KeyManager
from src.secure_channel import SecureChannel
import json, sys

km = KeyManager()
sc = SecureChannel(km)

with open('$1', 'r') as f:
    data = json.load(f)

msg = sc.receive_message(data, '$USER')
if msg:
    print('📖 Mensaje recibido:', msg)
else:
    print('❌ Error al descifrar mensaje')
"
```

---

## 📋 **Troubleshooting**

### **Problema: "Public key not found"**
**Solución:** Asegúrate de importar la clave pública del remitente antes de descifrar

### **Problema: "Signature verification failed"**
**Solución:** El archivo fue modificado o corrompido durante la transferencia

### **Problema: "User not found"**
**Solución:** Crea el usuario local o verifica el nombre exacto

### **Problema: Archivos no se transfieren**
**Solución:** Verifica permisos de archivos y métodos de transferencia

---

## 📖 **Ejemplos Prácticos**

### **Ejemplo 1: Universidad → Casa**
1. En universidad: Crear mensaje para "casa"
2. Enviar archivo por email
3. En casa: Descargar y descifrar

### **Ejemplo 2: Trabajo → Personal**
1. En trabajo: Mensaje para "personal"
2. Subir a Google Drive
3. En personal: Descargar y descifrar

### **Ejemplo 3: Múltiples Ubicaciones**
1. Crear grupos de usuarios
2. Intercambiar claves en cadena
3. Mensajes seguros entre todos

---

**🔐 ¡Comunicación segura entre máquinas con CipherChat!**


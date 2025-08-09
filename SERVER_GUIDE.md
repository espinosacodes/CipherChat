# 🌐 Guía del Servidor CipherChat

Esta guía explica cómo configurar y usar el servidor CipherChat para comunicación en tiempo real entre múltiples máquinas.

## 🚀 **Inicio Rápido**

### **Ejecutar el Servidor**
```bash
# Activar entorno virtual
source cipherchat_env/bin/activate

# Ejecutar servidor
python simple_server.py
```

**Estado:** ✅ **Servidor ejecutándose en puerto 8888**

## 🏗️ **Arquitectura del Sistema**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente A     │    │     Servidor    │    │   Cliente B     │
│    (Alice)      │    │   CipherChat    │    │     (Bob)       │
│                 │    │                 │    │                 │
│ 1. Cifra msg    │───▶│ 2. Relay msg    │───▶│ 3. Guarda msg   │
│ 4. Envía        │    │ 5. Sin descifr. │    │ 6. Descifra     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Características del Servidor:**
- 🔒 **No descifra mensajes** - Solo hace relay
- 🌐 **Múltiples clientes** - Soporta varios usuarios simultáneos
- 📡 **Tiempo real** - Entrega inmediata de mensajes
- 🛡️ **Seguro** - Los mensajes permanecen cifrados

## 🔗 **Conectar Clientes**

### **Desde la Misma Máquina (Prueba)**
```bash
python simple_server.py client
```

### **Desde Otra Máquina**
```bash
python connect_to_server.py <IP_SERVIDOR>
```

**IP del servidor actual:** `172.23.79.32:8888`

## 📋 **Comandos del Cliente**

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `list` | Mostrar usuarios conectados | `list` |
| `send <user> <file>` | Enviar mensaje cifrado | `send bob message.json` |
| `help` | Mostrar ayuda | `help` |
| `quit` | Desconectar | `quit` |

## 🔄 **Flujo de Trabajo Completo**

### **1. Preparación (Una sola vez)**

**En cada máquina cliente:**
```bash
# Instalar CipherChat completo
git clone <repository>
cd CipherChat
python setup.py

# Crear usuarios e intercambiar claves públicas
python cipherchat.py
```

### **2. Configurar Servidor**

**En máquina servidor:**
```bash
# Ejecutar servidor CipherChat
python simple_server.py
```

### **3. Conectar Clientes**

**En cada máquina cliente:**
```bash
# Conectar al servidor
python connect_to_server.py <SERVER_IP>
```

### **4. Comunicación**

**Enviar mensaje:**
1. **Crear mensaje cifrado:**
   ```bash
   python cipherchat.py
   # Opción 3: Send Message
   # Resultado: archivo .json con mensaje cifrado
   ```

2. **Enviar via red:**
   ```bash
   # En cliente de red
   send bob alice_to_bob_20240115_143022.json
   ```

**Recibir mensaje:**
1. **Automático** - El archivo se guarda en `received_messages/`
2. **Descifrar:**
   ```bash
   python cipherchat.py
   # Opción 4: Receive Message
   # Seleccionar archivo recibido
   ```

## 🔧 **Configuración Avanzada**

### **Cambiar Puerto**
```python
# En simple_server.py, línea ~15
def __init__(self, host='localhost', port=9999):  # Cambiar puerto
```

### **Permitir Conexiones Externas**
```python
# En simple_server.py, línea ~15  
def __init__(self, host='0.0.0.0', port=8888):  # Escuchar todas las IPs
```

### **Configurar Firewall**

**Linux:**
```bash
sudo ufw allow 8888
```

**Windows:**
```cmd
netsh advfirewall firewall add rule name="CipherChat" dir=in action=allow protocol=TCP localport=8888
```

## 🚨 **Troubleshooting**

### **"Connection refused"**
- ✅ Verificar que el servidor esté ejecutándose
- ✅ Comprobar que el puerto 8888 esté abierto
- ✅ Verificar firewall

### **"User not connected"**
- ✅ Destinatario debe estar conectado al servidor
- ✅ Verificar nombre de usuario exacto

### **"Message not decrypting"**
- ✅ Asegurar intercambio de claves completado
- ✅ Verificar que el archivo no esté corrupto

## 🔐 **Consideraciones de Seguridad**

### **✅ Seguro:**
- Mensajes permanecen cifrados en tránsito
- Servidor no tiene acceso a claves privadas
- Autenticación por firmas digitales

### **⚠️ Consideraciones:**
- Servidor puede ver metadatos (quién envía a quién)
- Requiere confianza en el operador del servidor
- Conexiones no cifradas al servidor (usar VPN para mayor seguridad)

### **🛡️ Recomendaciones:**
- Usar servidor propio o de confianza
- Considerar VPN para conexiones adicionales
- Verificar identidades por canal secundario

## 📊 **Monitoreo del Servidor**

### **Ver Conexiones Activas**
```bash
netstat -an | grep :8888
```

### **Ver Logs del Servidor**
Los mensajes aparecen en la consola del servidor:
- `✅ User 'alice' registered`
- `📤 Message relayed: alice → bob`
- `👋 User 'bob' disconnected`

## 🚀 **Instalación Rápida para Clientes**

Para configurar clientes rápidamente en otras máquinas:

```bash
python quick_client_setup.py
```

Esto crea una instalación mínima con:
- Cliente de red
- Dependencias básicas
- Scripts de inicio
- Instrucciones de uso

## 📈 **Escalabilidad**

### **Límites Actuales:**
- ~50 usuarios simultáneos (hardware dependiente)
- Sin persistencia de mensajes
- Single-threaded por cliente

### **Mejoras Futuras:**
- Base de datos para mensajes offline
- Balanceador de carga
- Cifrado TLS para conexiones
- Autenticación de servidor

## 🎯 **Casos de Uso**

### **1. Equipo de Trabajo Remoto**
- Servidor en oficina central
- Clientes en casa de empleados
- Comunicación segura de documentos

### **2. Comunicación Familiar**
- Servidor en casa principal
- Familiares conectan desde ubicaciones diferentes
- Mensajes privados seguros

### **3. Grupos de Estudio**
- Servidor temporal para proyectos
- Estudiantes desde diferentes universidades
- Intercambio seguro de información

---

**🌐 ¡Servidor CipherChat ejecutándose y listo para conexiones!**

**Estado:** ✅ **Activo en puerto 8888**  
**IP:** `172.23.79.32`  
**Comando cliente:** `python connect_to_server.py 172.23.79.32`

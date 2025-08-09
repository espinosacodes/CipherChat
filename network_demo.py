#!/usr/bin/env python3
"""
CipherChat Network Demo
Demonstrates how to use CipherChat across different machines using file transfer.
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.key_manager import KeyManager
from src.secure_channel import SecureChannel

def setup_machine_demo():
    """Setup demo for two-machine communication."""
    print("🌐 CipherChat Multi-Machine Setup Demo")
    print("=" * 50)
    
    # Create separate directories for each "machine"
    machine1_dir = Path("machine1_simulation")
    machine2_dir = Path("machine2_simulation")
    shared_dir = Path("shared_transfer")  # Simulates file transfer between machines
    
    # Clean and create directories
    for dir_path in [machine1_dir, machine2_dir, shared_dir]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir()
    
    print(f"📁 Created simulation directories:")
    print(f"   Machine 1: {machine1_dir}")
    print(f"   Machine 2: {machine2_dir}")
    print(f"   Shared Transfer: {shared_dir}")
    
    return machine1_dir, machine2_dir, shared_dir

def machine1_setup(machine1_dir, shared_dir):
    """Setup for Machine 1 (Alice)."""
    print("\n💻 MACHINE 1 SETUP (Alice)")
    print("-" * 30)
    
    # Initialize Alice's environment
    key_manager1 = KeyManager(str(machine1_dir / "keys"))
    secure_channel1 = SecureChannel(key_manager1)
    
    # Generate Alice's keys
    print("🔑 Generating Alice's keys...")
    key_manager1.generate_user_keys("alice")
    
    # Export Alice's public key for sharing
    alice_public_export = shared_dir / "alice_public_key.pem"
    key_manager1.export_public_key("alice", str(alice_public_export))
    
    # Create key exchange message
    print("📤 Creating key exchange message...")
    key_exchange = secure_channel1.create_key_exchange_message("alice", "bob")
    with open(shared_dir / "alice_key_exchange.json", 'w') as f:
        json.dump(key_exchange, f, indent=2)
    
    print("✅ Machine 1 setup complete!")
    print(f"📄 Files ready for transfer:")
    print(f"   - {alice_public_export}")
    print(f"   - {shared_dir / 'alice_key_exchange.json'}")
    
    return key_manager1, secure_channel1

def machine2_setup(machine2_dir, shared_dir):
    """Setup for Machine 2 (Bob)."""
    print("\n💻 MACHINE 2 SETUP (Bob)")
    print("-" * 30)
    
    # Initialize Bob's environment
    key_manager2 = KeyManager(str(machine2_dir / "keys"))
    secure_channel2 = SecureChannel(key_manager2)
    
    # Generate Bob's keys
    print("🔑 Generating Bob's keys...")
    key_manager2.generate_user_keys("bob")
    
    # Export Bob's public key for sharing
    bob_public_export = shared_dir / "bob_public_key.pem"
    key_manager2.export_public_key("bob", str(bob_public_export))
    
    # Import Alice's public key (simulate receiving it)
    alice_public_file = shared_dir / "alice_public_key.pem"
    if alice_public_file.exists():
        print("📥 Importing Alice's public key...")
        key_manager2.import_public_key("alice", str(alice_public_file))
    
    # Process Alice's key exchange
    alice_key_exchange_file = shared_dir / "alice_key_exchange.json"
    if alice_key_exchange_file.exists():
        print("🔄 Processing Alice's key exchange...")
        with open(alice_key_exchange_file, 'r') as f:
            alice_key_exchange = json.load(f)
        secure_channel2.process_key_exchange(alice_key_exchange)
    
    # Create Bob's key exchange message
    print("📤 Creating Bob's key exchange message...")
    key_exchange = secure_channel2.create_key_exchange_message("bob", "alice")
    with open(shared_dir / "bob_key_exchange.json", 'w') as f:
        json.dump(key_exchange, f, indent=2)
    
    print("✅ Machine 2 setup complete!")
    print(f"📄 Files ready for transfer:")
    print(f"   - {bob_public_export}")
    print(f"   - {shared_dir / 'bob_key_exchange.json'}")
    
    return key_manager2, secure_channel2

def complete_machine1_setup(key_manager1, secure_channel1, shared_dir):
    """Complete Machine 1 setup after receiving Bob's files."""
    print("\n💻 MACHINE 1 - RECEIVING BOB'S KEY")
    print("-" * 35)
    
    # Import Bob's public key
    bob_public_file = shared_dir / "bob_public_key.pem"
    if bob_public_file.exists():
        print("📥 Importing Bob's public key...")
        key_manager1.import_public_key("bob", str(bob_public_file))
    
    # Process Bob's key exchange
    bob_key_exchange_file = shared_dir / "bob_key_exchange.json"
    if bob_key_exchange_file.exists():
        print("🔄 Processing Bob's key exchange...")
        with open(bob_key_exchange_file, 'r') as f:
            bob_key_exchange = json.load(f)
        secure_channel1.process_key_exchange(bob_key_exchange)
    
    print("✅ Key exchange completed on Machine 1!")

def demonstrate_cross_machine_messaging(secure_channel1, secure_channel2, shared_dir):
    """Demonstrate messaging between the two machines."""
    print("\n💬 CROSS-MACHINE MESSAGING DEMO")
    print("-" * 35)
    
    # Alice sends message to Bob
    print("📤 Alice (Machine 1) sends message to Bob (Machine 2)...")
    alice_message = "Hello Bob! This secure message travels between machines! 🌐"
    encrypted_msg = secure_channel1.send_message("alice", "bob", alice_message)
    
    if encrypted_msg:
        # Save encrypted message to shared transfer
        msg_file = shared_dir / "alice_to_bob_message.json"
        with open(msg_file, 'w') as f:
            f.write(secure_channel1.export_message_for_transmission(encrypted_msg))
        
        print(f"💾 Message saved to: {msg_file}")
        print(f"📝 Original message: '{alice_message}'")
        
        # Bob receives and decrypts the message (on Machine 2)
        print("\n📥 Bob (Machine 2) receives and decrypts message...")
        with open(msg_file, 'r') as f:
            received_data = json.load(f)
        
        decrypted_msg = secure_channel2.receive_message(received_data, "bob")
        if decrypted_msg:
            print(f"📖 Bob decrypted: '{decrypted_msg}'")
            print("✅ Cross-machine communication successful!")
            
            # Bob replies to Alice
            print("\n📤 Bob replies to Alice...")
            bob_reply = "Hi Alice! I received your cross-machine message perfectly! 👍"
            encrypted_reply = secure_channel2.send_message("bob", "alice", bob_reply)
            
            if encrypted_reply:
                reply_file = shared_dir / "bob_to_alice_reply.json"
                with open(reply_file, 'w') as f:
                    f.write(secure_channel2.export_message_for_transmission(encrypted_reply))
                
                print(f"💾 Reply saved to: {reply_file}")
                
                # Alice receives Bob's reply
                print("\n📥 Alice receives Bob's reply...")
                with open(reply_file, 'r') as f:
                    reply_data = json.load(f)
                
                decrypted_reply = secure_channel1.receive_message(reply_data, "alice")
                if decrypted_reply:
                    print(f"📖 Alice received: '{decrypted_reply}'")
                    print("✅ Two-way cross-machine communication complete!")

def show_manual_instructions():
    """Show instructions for manual setup across real machines."""
    print("\n📋 INSTRUCCIONES PARA MÁQUINAS REALES")
    print("=" * 50)
    
    print("""
🖥️  MÁQUINA 1 (Alice):
1. Instalar CipherChat:
   git clone <repo>
   cd CipherChat
   python setup.py

2. Crear usuario y generar claves:
   python cipherchat.py
   → Opción 1 (User Management) → 1 (Create New User) → "alice"
   → Opción 1 → 2 (Select User) → alice

3. Exportar clave pública:
   → Opción 2 (Key Management) → 1 (Export My Public Key)
   → Archivo: alice_public.pem

4. Crear mensaje de intercambio de claves:
   → Opción 5 (Key Exchange) → 1 (Send my public key)
   → Recipient: bob
   → Archivo: key_exchange_alice_to_bob.json

5. Transferir archivos a Máquina 2:
   - alice_public.pem
   - key_exchange_alice_to_bob.json

---

🖥️  MÁQUINA 2 (Bob):
1. Instalar CipherChat (igual que Máquina 1)

2. Crear usuario "bob" y seleccionarlo

3. Importar clave pública de Alice:
   → Opción 2 → 2 (Import Someone's Public Key)
   → Username: alice
   → File: alice_public.pem

4. Procesar intercambio de claves:
   → Opción 5 → 2 (Process received key exchange)
   → File: key_exchange_alice_to_bob.json

5. Crear respuesta de intercambio:
   → Opción 5 → 1 (Send my public key)
   → Recipient: alice

6. Transferir archivos a Máquina 1:
   - bob_public.pem
   - key_exchange_bob_to_alice.json

---

🔄 FINALIZAR EN MÁQUINA 1:
- Importar clave de Bob y procesar su intercambio

---

💬 ENVIAR MENSAJES:
- Opción 3 (Send Message) → Recipient + Message
- Archivo generado se transfiere a la otra máquina
- Opción 4 (Receive Message) → Seleccionar archivo recibido

---

📁 MÉTODOS DE TRANSFERENCIA:
• USB/Pendrive    • Email (archivos adjuntos)
• Google Drive    • Telegram/WhatsApp
• WeTransfer      • SSH/SCP
• Dropbox         • Cualquier método de archivos
""")

def main():
    """Main demo function."""
    try:
        # Setup simulation
        machine1_dir, machine2_dir, shared_dir = setup_machine_demo()
        
        # Setup both machines
        key_manager1, secure_channel1 = machine1_setup(machine1_dir, shared_dir)
        key_manager2, secure_channel2 = machine2_setup(machine2_dir, shared_dir)
        
        # Complete Alice's setup
        complete_machine1_setup(key_manager1, secure_channel1, shared_dir)
        
        # Demonstrate messaging
        demonstrate_cross_machine_messaging(secure_channel1, secure_channel2, shared_dir)
        
        # Show manual instructions
        show_manual_instructions()
        
        print("\n🎉 DEMO COMPLETADO")
        print("=" * 50)
        print("✅ Simulación de comunicación entre máquinas exitosa")
        print("📂 Archivos de simulación guardados en:")
        print(f"   - {machine1_dir}")
        print(f"   - {machine2_dir}")
        print(f"   - {shared_dir}")
        
    except Exception as e:
        print(f"❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


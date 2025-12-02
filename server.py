#!/usr/bin/env python3
"""
TCP Server for IoT Temperature Monitoring
TELE 6550 Project - Desktop Application

This server receives temperature data from an ESP32 device
and displays it on the console in real-time.
"""

import socket
import sys
from datetime import datetime

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 9000       # Port to listen on (must match ESP32 configuration)

def main():
    """Main server function to receive and display temperature data"""
    
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        
        print("=" * 60)
        print("IoT Temperature Monitoring Server")
        print("=" * 60)
        print(f"Server listening on {HOST}:{PORT}")
        print("Waiting for ESP32 connection...\n")
        
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f"✓ Connected to ESP32 at {client_address[0]}:{client_address[1]}")
        print("=" * 60)
        print("Receiving temperature data:\n")
        
        # Receive data from the client
        buffer = ""
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                print("\n✗ Connection closed by ESP32")
                break
            
            # Decode received data and add to buffer
            buffer += data.decode('utf-8')
            
            # Process complete lines
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line.strip():
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    print(f"[{timestamp}] {line}")
                    sys.stdout.flush()  # Ensure immediate output
    
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped by user")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    finally:
        # Clean up connections
        try:
            client_socket.close()
        except:
            pass
        server_socket.close()
        print("Server socket closed")

if __name__ == "__main__":
    main()

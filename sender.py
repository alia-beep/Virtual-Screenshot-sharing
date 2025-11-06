import socket
import struct
import pickle
import cv2
import numpy as np
from PIL import ImageGrab

# ===== Sender (Server) Setup =====
SERVER_IP = socket.gethostbyname(socket.gethostname())  # Automatically get local IP
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(1)

print(f"[SENDER] Server started on {SERVER_IP}:{PORT}")
print("[SENDER] Waiting for receiver to connect...")

client_socket, addr = server_socket.accept()
print(f"[SENDER] Receiver connected from {addr}")

# ===== Sending Screenshots in Real-Time =====
try:
    while True:
        # Capture screen using PIL
        img = ImageGrab.grab()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Serialize the frame
        data = pickle.dumps(frame)
        message_size = struct.pack("Q", len(data))

        # Send message length first, then data
        client_socket.sendall(message_size + data)

        # Display the frame being sent (optional)
        cv2.imshow("SENDER - Sharing Screen", frame)
        if cv2.waitKey(1) == 13:  # Press Enter to stop
            break

except Exception as e:
    print(f"[ERROR] {e}")

finally:
    client_socket.close()
    server_socket.close()
    cv2.destroyAllWindows()
    print("[SENDER] Connection closed.")

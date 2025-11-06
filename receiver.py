import socket
import struct
import pickle
import cv2

# ===== Receiver (Client) Setup =====
SERVER_IP = input("Enter Sender (Server) IP Address: ").strip()
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f"[RECEIVER] Connected to sender at {SERVER_IP}:{PORT}")

data = b""
payload_size = struct.calcsize("Q")

# ===== Receiving and Displaying Frames =====
try:
    while True:
        # Retrieve message size
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Retrieve all frame data
        while len(data) < msg_size:
            data += client_socket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize and display the frame
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVER - Live Screen", frame)

        if cv2.waitKey(1) == 13:  # Press Enter to exit
            break

except Exception as e:
    print(f"[ERROR] {e}")

finally:
    client_socket.close()
    cv2.destroyAllWindows()
    print("[RECEIVER] Connection closed.")

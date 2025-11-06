import cv2
import mediapipe as mp
import numpy as np
import time

class GestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.bg_color = (0, 0, 0)
        self.object_position = [320, 240]
        self.scene = 0
        self.scene_names = ["Mover Objeto", "Cambiar Color", "Dibujar"]
        self.prev_hand_gesture = None
        self.gesture_cooldown = 0

        self.drawing_points = []
        self.is_drawing = False
        self.draw_color = (0, 255, 0)

    def process_frame(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape
        results = self.hands.process(image_rgb)
        overlay = frame.copy()

        if self.scene == 1:
            cv2.rectangle(overlay, (0, 0), (w, h), self.bg_color, -1)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    overlay,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )

                if self.scene == 0:
                    self.handle_move_object(hand_landmarks, w, h)
                elif self.scene == 1:
                    self.handle_change_color(hand_landmarks)
                elif self.scene == 2:
                    self.handle_drawing(hand_landmarks, overlay, w, h)

                if time.time() > self.gesture_cooldown:
                    current_gesture = self.detect_open_palm(hand_landmarks)
                    if current_gesture == "open_palm" and self.prev_hand_gesture != "open_palm":
                        self.scene = (self.scene + 1) % len(self.scene_names)
                        self.gesture_cooldown = time.time() + 1.5
                        self.drawing_points = []
                    self.prev_hand_gesture = current_gesture

        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

        if self.scene == 0:
            cv2.circle(frame, (self.object_position[0], self.object_position[1]), 30, (0, 0, 255), -1)
        elif self.scene == 2:
            if len(self.drawing_points) > 1:
                for i in range(1, len(self.drawing_points)):
                    if self.drawing_points[i-1] and self.drawing_points[i]:
                        cv2.line(frame, self.drawing_points[i-1], self.drawing_points[i], self.draw_color, 5)

        cv2.putText(frame, f"Escena: {self.scene_names[self.scene]}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        if self.scene == 0:
            cv2.putText(frame, "Mueve el indice para controlar el circulo", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        elif self.scene == 1:
            cv2.putText(frame, "Abre/cierra la mano para cambiar color", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        elif self.scene == 2:
            cv2.putText(frame, "Indice+pulgar juntos para dibujar", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Muestra la palma abierta para cambiar de escena", (10, h-30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return frame

    def handle_move_object(self, hand_landmarks, width, height):
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x, y = int(index_tip.x * width), int(index_tip.y * height)
        self.object_position = [x, y]

    def handle_change_color(self, hand_landmarks):
        fingers_extended = self.count_fingers_extended(hand_landmarks)
        colors = {
            0: (0, 0, 0),      # Negro
            1: (0, 0, 255),    # Rojo
            2: (0, 255, 0),    # Verde
            3: (255, 0, 0),    # Azul
            4: (0, 255, 255),  # Amarillo
            5: (255, 0, 255)   # Magenta
        }
        self.bg_color = colors.get(fingers_extended, (0, 0, 0))

    def handle_drawing(self, hand_landmarks, frame, width, height):
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)
        thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
        distance = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5
        if distance < 40:
            if not self.is_drawing:
                self.is_drawing = True
                self.drawing_points.append(None)
            else:
                self.drawing_points.append((index_x, index_y))
        else:
            self.is_drawing = False

    def count_fingers_extended(self, hand_landmarks):
        finger_tips = [
            self.mp_hands.HandLandmark.THUMB_TIP,
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_hands.HandLandmark.RING_FINGER_TIP,
            self.mp_hands.HandLandmark.PINKY_TIP
        ]
        finger_pips = [
            self.mp_hands.HandLandmark.THUMB_IP,
            self.mp_hands.HandLandmark.INDEX_FINGER_PIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
            self.mp_hands.HandLandmark.RING_FINGER_PIP,
            self.mp_hands.HandLandmark.PINKY_PIP
        ]
        count = 0
        thumb_tip = hand_landmarks.landmark[finger_tips[0]]
        thumb_base = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_CMC]
        if thumb_tip.x < thumb_base.x:
            count += 1
        for i in range(1, 5):
            tip = hand_landmarks.landmark[finger_tips[i]]
            pip = hand_landmarks.landmark[finger_pips[i]]
            if tip.y < pip.y:
                count += 1
        return count

    def detect_open_palm(self, hand_landmarks):
        fingers = self.count_fingers_extended(hand_landmarks)
        return "open_palm" if fingers >= 4 else "other"

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    # Configurar grabación de video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('prueba_gestos.mp4', fourcc, fps, (width, height))
    print("🎥 Grabando video en 'prueba_gestos.mp4'... (presiona ESC para detener)")

    gesture_controller = GestureController()

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        output_frame = gesture_controller.process_frame(frame)
        cv2.imshow('Control por Gestos - MediaPipe', output_frame)

        # Grabar el frame procesado
        out.write(output_frame)

        if cv2.waitKey(5) & 0xFF == 27:  # ESC para salir
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("✅ Grabación finalizada. Video guardado como 'prueba_gestos.mp4'.")

if __name__ == "__main__":
    main()

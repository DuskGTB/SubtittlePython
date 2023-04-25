import cv2
import threading
import speech_recognition as sr

# Fonction pour écouter et transcrire l'audio en temps réel
def listen_and_transcribe(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language='fr-FR')
        print("Vous avez dit: " + text)
        return text
    except sr.UnknownValueError:
        return ""

def process_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Ajustement du bruit ambiant...")
        recognizer.adjust_for_ambient_noise(source)

    while True:
        print("Écoute...")
        audio = recognizer.listen(microphone, timeout=2)
        threading.Thread(target=listen_and_transcribe, args=(recognizer, audio)).start()

def display_camera():
    # Initialisation de la fenêtre
    window_name = "Video avec sous-titres"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 640, 480)

    # Accès à la caméra
    cap = cv2.VideoCapture(0)

    # Vérification si la caméra est ouverte
    if not cap.isOpened():
        print("Erreur: Impossible d'accéder à la caméra.")
        exit()

    while True:
        # Capture et affichage des images de la caméra
        ret, frame = cap.read()
        if not ret:
            print("Erreur: Impossible de lire les images de la caméra.")
            break

        cv2.imshow(window_name, frame)

        # Fermeture de la fenêtre si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libération des ressources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    threading.Thread(target=process_audio).start()
    display_camera()
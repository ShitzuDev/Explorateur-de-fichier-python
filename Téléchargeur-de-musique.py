import os
import yt_dlp
import time
from colorama import Fore, Style, init

# Initialiser colorama
init(autoreset=True)

def animated_text(text, color=Fore.MAGENTA, delay=0.05):
    """
    Affiche un texte lettre par lettre avec une couleur et un délai, sauf pour les lignes contenant '==='.
    :param text: Texte à afficher.
    :param color: Couleur du texte (par défaut magenta).
    :param delay: Temps entre chaque lettre (en secondes).
    """
    if "===" in text:
        # Afficher directement les lignes avec '===' sans animation
        print(color + text + Style.RESET_ALL)
    else:
        for char in text:
            print(color + char, end="", flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)  # Réinitialiser le style à la fin

def show_welcome_message():
    welcome_message = """
===============================================================
  Ce programme a été créé par Shitzu.
  Si vous rencontrez des problèmes, tout est expliqué sur :
  - Notre serveur Discord : https://discord.gg/votre_lien
  - Notre GitHub : https://github.com/shitzu-dev

  ! Ne tenez pas compte du message d'erreur, la musique sera tout de même téléchargée avec succès!
  
  Merci d'utiliser notre téléchargeur de musique !
===============================================================
"""
    animated_text(welcome_message, color=Fore.MAGENTA)

def download_music(search_query, output_folder="Musiques"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": False,
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0"
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        animated_text(f"\nRecherche et téléchargement de : {search_query}\n", color=Fore.CYAN)
        try:
            ydl.download([f"ytsearch:{search_query}"])
            animated_text(f"Musique téléchargée dans : {output_folder}\n", color=Fore.GREEN)
        except Exception as e:
            animated_text(f"Erreur lors du téléchargement : {e}\n", color=Fore.RED)

def main():
    show_welcome_message()
    animated_text("=== Téléchargeur de Musique Automatique ===\n", color=Fore.YELLOW)
    print("\nEntrez le titre ou l'artiste de la chanson que vous voulez télécharger.")
    print("Tapez 'exit' pour quitter.\n")

    while True:
        search_query = input(Fore.BLUE + "Entrez le titre ou l'artiste (ou 'exit' pour quitter) : ").strip()
        if search_query.lower() == "exit":
            animated_text("Merci d'avoir utilisé le téléchargeur de musique !", color=Fore.YELLOW)
            break

        # Télécharger la musique basée sur la recherche
        download_music(search_query)

if __name__ == "__main__":
    main()

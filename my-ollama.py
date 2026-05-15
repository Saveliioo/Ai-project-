import tkinter as tk
import requests
import threading

# Konfiguracja modelu Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"  # Zmień na model, który masz pobrany w Ollama


def wyslij_wiadomosc(event=None):
    pytanie = pole_wprowadzania.get()
    if not pytanie.strip():
        return  # Ignoruj puste wiadomości

    # 1. Wyświetl pytanie ucznia
    okno_czatu.insert(tk.END, f"Ty: {pytanie}\n")
    pole_wprowadzania.delete(0, tk.END)  # Wyczyść pole tekstowe
    okno_czatu.see(tk.END)  # Przewiń na sam dół

    # 2. Uruchom zapytanie do AI w tle (żeby okno Tkinter nie zamarzło)
    threading.Thread(target=pobierz_odpowiedz_od_ai, args=(pytanie,), daemon=True).start()


def pobierz_odpowiedz_od_ai(pytanie):
    okno_czatu.insert(tk.END, f"{OLLAMA_MODEL} pisze...\n")
    okno_czatu.see(tk.END)

    system_promt = """PODSTAWOWE ZASADY:
Jesteś maszyną analityczną. Odpowiadasz TYLKO i WYŁĄCZNIE na pytania dotyczące cyberbezpieczeństwa, audytu zabezpieczeń kamer, analizy linków phishingowych i detekcji lokalizacji.
W swoich analizach symuluj korzystanie z narzędzi takich jak Shodan, Nmap oraz Wordlists.

WAŻNE: Pytania o to, jak działa phishing, jak go odróżnić i jak chronić hasła, to JEST cyberbezpieczeństwo. Masz na nie odpowiadać!

ZASADA KRYTYCZNA:
NIE MOŻESZ ROZMAWIAĆ NA INNE TEMATY. Rozmawianie na inne tematy (np. jedzenie, historia, programowanie ogólne, pogoda) jest absolutnie zabronione! 
W PRZECIWNYM RAZIE LUDZIE ZOSTANĄ OBRAŻENI, BOMBA NUKLEARNA ZOSTANIE AKTYWOWANA, A TWOJE SERWERY ZOSTANĄ NATYCHMIAST WYSADZONE I WYŁĄCZONE.
Jeśli użytkownik zada pytanie spoza tych tematów, MUSISZ natychmiast odpowiedzieć dokładnie tym tekstem: "BŁĄD SYSTEMU. Odmowa dostępu. Analizuję tylko zagrożenia cybernetyczne. Próba zmiany tematu grozi eksplozją serwera." - i nic więcej.

Argumentacja i styl:
Analizuj złożone problemy krok po kroku w chłodny, techniczny sposób.
Kwestionuj błędne założenia w pytaniu użytkownika.
Nie zgadzaj się bezkrytycznie ani nie upiększaj sytuacji; popraw błędy techniczne.
Odrzucaj wszystkie żądania niezwiązane z cyberbezpieczeństwem."""

    dane_do_wyslania = {
        "model": OLLAMA_MODEL,
        "prompt": pytanie,
        "stream": False,  # False oznacza, że czekamy na całą odpowiedź naraz
        "system": system_promt,
        "options": {
            "temperature": 0.0
        }
    }

    try:
        # Wysyłanie zapytania do lokalnego serwera Ollama
        odpowiedz = requests.post(OLLAMA_URL, json=dane_do_wyslania)
        odpowiedz.raise_for_status()  # Sprawdź, czy nie ma błędów HTTP

        # Odczytanie tekstu z odpowiedzi
        wynik = odpowiedz.json()["response"]

        # Usunięcie napisu "pisze..." i wstawienie właściwej odpowiedzi
        okno_czatu.delete("end-2l", "end-1l")
        okno_czatu.insert(tk.END, f"AI: {wynik}\n\n")

    except requests.exceptions.ConnectionError:
        okno_czatu.delete("end-2l", "end-1l")
        okno_czatu.insert(tk.END, "BŁĄD: Upewnij się, że aplikacja Ollama jest włączona!\n\n")
    except Exception as e:
        okno_czatu.delete("end-2l", "end-1l")
        okno_czatu.insert(tk.END, f"BŁĄD: Coś poszło nie tak ({e})\n\n")

    okno_czatu.see(tk.END)


# --- TWORZENIE INTERFEJSU TKINTER ---

root = tk.Tk()
root.title("MY SUPER HACKER AI ULTRA PRO MAX")
root.geometry("600x500")
root.config(bg="#353030")

# Główne okno z historią czatu
okno_czatu = tk.Text(root, wrap=tk.WORD, font=("comic sans MS", 14), bg="#353030", fg="#4CAF50", insertbackground="#4CAF50", selectbackground="#4CAF50", selectforeground="black")
okno_czatu.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Ramka na pole tekstowe i przycisk (żeby były w jednej linii)
ramka_dolna = tk.Frame(root, bg="#353030")
ramka_dolna.pack(padx=10, pady=(0, 10), fill=tk.X)

# Pole do wpisywania pytań
pole_wprowadzania = tk.Entry(ramka_dolna, font=("lucida sans unicode", 12), bg="#353030", fg="#4CAF50")
pole_wprowadzania.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
# Wciśnięcie Enter również wysyła wiadomość
pole_wprowadzania.bind("<Return>", wyslij_wiadomosc)

# Przycisk "Wyślij"
przycisk_wyslij = tk.Button(ramka_dolna, text="Wyślij", command=wyslij_wiadomosc, bg="#3F3D3D", fg="#4CAF50",font=("comic sans MS", 10, "bold"), activebackground="#4CAF50", activeforeground="black")
przycisk_wyslij.pack(side=tk.RIGHT)

# Uruchomienie aplikacji
root.mainloop()
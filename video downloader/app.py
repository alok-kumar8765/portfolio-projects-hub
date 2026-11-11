import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp


class YouTubeDownloaderApp:

  def __init__(self, root):
    self.root = root
    self.root.title("YouTube Video Downloader")
    self.root.geometry("600x500")
    self.root.configure(bg="#0f0f0f")
    self.root.resizable(False, False)

    # Style Configuration for Dark Theme
    self.style = ttk.Style()
    self.style.theme_use("clam")
    self.style.configure(
        "TCombobox",
        fieldbackground="#1f1f1f",
        background="#2f2f2f",
        foreground="white",
        selectbackground="#e63946",
    )
    self.style.configure(
        "Horizontal.TProgressbar",
        troughcolor="#1f1f1f",
        background="#e63946",
        darkcolor="#e63946",
        lightcolor="#e63946",
    )

    # Title Label
    title_label = tk.Label(
        root,
        text="YouTube Downloader",
        font=("Arial", 18, "bold"),
        bg="#0f0f0f",
        fg="white",
    )
    title_label.pack(pady=15)

    # Main Frame
    main_frame = tk.Frame(root, bg="#0f0f0f")
    main_frame.pack(padx=20, pady=5, fill="x")

    # URL Entry
    tk.Label(
        main_frame,
        text="Video URL",
        font=("Arial", 10, "bold"),
        bg="#0f0f0f",
        fg="#aaaaaa",
    ).pack(anchor="w")
    self.url_entry = tk.Entry(
        main_frame,
        font=("Arial", 11),
        bg="#1f1f1f",
        fg="white",
        insertbackground="white",
        relief="flat",
    )
    self.url_entry.pack(fill="x", pady=(5, 15), ipady=5)

    # Save Location
    tk.Label(
        main_frame,
        text="Save Location",
        font=("Arial", 10, "bold"),
        bg="#0f0f0f",
        fg="#aaaaaa",
    ).pack(anchor="w")

    path_frame = tk.Frame(main_frame, bg="#0f0f0f")
    path_frame.pack(fill="x", pady=(5, 15))

    self.path_entry = tk.Entry(
        path_frame,
        font=("Arial", 11),
        bg="#1f1f1f",
        fg="white",
        insertbackground="white",
        relief="flat",
    )
    self.path_entry.pack(side="left", fill="x", expand=True, ipady=5)
    self.path_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))

    browse_btn = tk.Button(
        path_frame,
        text="Browse",
        command=self.browse_path,
        bg="#457b9d",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
    )
    browse_btn.pack(side="right", padx=(10, 0), ipadx=10, ipady=3)

    # Format Selection Dropdown
    tk.Label(
        main_frame,
        text="Download Format",
        font=("Arial", 10, "bold"),
        bg="#0f0f0f",
        fg="#aaaaaa",
    ).pack(anchor="w")

    self.format_var = tk.StringVar(value="Best Video (MP4)")
    self.format_combobox = ttk.Combobox(
        main_frame,
        textvariable=self.format_var,
        values=[
            "Best Video (MP4)",
            "Audio Only (MP3)",
            "Highest Quality (Any)",
        ],
        state="readonly",
        font=("Arial", 10),
    )
    self.format_combobox.pack(fill="x", pady=(5, 20), ipady=3)

    # Action Buttons Frame
    btn_frame = tk.Frame(main_frame, bg="#0f0f0f")
    btn_frame.pack(fill="x", pady=10)

    self.download_btn = tk.Button(
        btn_frame,
        text="Download",
        command=self.start_download_thread,
        bg="#e63946",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        cursor="hand2",
    )
    self.download_btn.pack(
        side="left", fill="x", expand=True, padx=(0, 5), ipady=8
    )

    clear_btn = tk.Button(
        btn_frame,
        text="Clear",
        command=self.clear_fields,
        bg="#1d3557",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        cursor="hand2",
    )
    clear_btn.pack(
        side="right", fill="x", expand=True, padx=(5, 0), ipadx=10, ipady=8
    )

    # Progress Bar & Status Section
    self.progress_var = tk.DoubleVar()
    self.progress_bar = ttk.Progressbar(
        main_frame,
        orient="horizontal",
        variable=self.progress_var,
        maximum=100,
        style="Horizontal.TProgressbar",
    )
    self.progress_bar.pack(fill="x", pady=(15, 5))

    self.status_var = tk.StringVar(value="Ready")
    status_label = tk.Label(
        main_frame,
        textvariable=self.status_var,
        font=("Arial", 9),
        bg="#0f0f0f",
        fg="#888888",
    )
    status_label.pack(anchor="w")

  def browse_path(self):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
      self.path_entry.delete(0, tk.END)
      self.path_entry.insert(0, folder_selected)

  def clear_fields(self):
    self.url_entry.delete(0, tk.END)
    self.progress_var.set(0)
    self.status_var.set("Ready")

  def progress_hook(self, d):
    if d["status"] == "downloading":
      total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
      downloaded = d.get("downloaded_bytes", 0)
      if total > 0:
        percent = (downloaded / total) * 100
        self.progress_var.set(percent)
        speed = d.get("_speed_str", "N/A")
        eta = d.get("_eta_str", "N/A")
        self.status_var.set(
            f"Downloading... {percent:.1f}% | Speed: {speed} | ETA: {eta}"
        )
    elif d["status"] == "finished":
      self.status_var.set("Download complete! Processing file...")

  def start_download_thread(self):
    url = self.url_entry.get().strip()
    if not url:
      messagebox.showerror("Error", "Please enter a valid YouTube URL!")
      return

    # Disable download button to prevent spam clicking
    self.download_btn.config(state="disabled", bg="#555555")
    self.progress_var.set(0)

    # Run in a separate thread so GUI doesn't freeze
    threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

  def download_video(self, url):
    path = self.path_entry.get().strip()
    format_choice = self.format_var.get()

    # Configure yt-dlp options based on dropdown choice
    ydl_opts = {
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "progress_hooks": [self.progress_hook],
    }

    if "Audio Only" in format_choice:
      ydl_opts["format"] = "bestaudio/best"
      ydl_opts["postprocessors"] = [{
          "key": "FFmpegExtractAudio",
          "preferredcodec": "mp3",
          "preferredquality": "192",
      }]
    elif "Best Video" in format_choice:
      ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    else:
      ydl_opts["format"] = "best"

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
      self.root.after(
          0, lambda: messagebox.showinfo("Success", "Download completed successfully!")
      )
      self.root.after(0, lambda: self.status_var.set("Ready"))
    except Exception as e:
      self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
      self.root.after(0, lambda: self.status_var.set("Download failed"))
    finally:
      # Re-enable download button
      self.root.after(
          0, lambda: self.download_btn.config(state="normal", bg="#e63946")
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = YouTubeDownloaderApp(root)
  root.mainloop()
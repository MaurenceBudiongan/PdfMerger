import customtkinter as ctk  
from tkinter import filedialog 
from PyPDF2 import PdfMerger
import os, webbrowser

# Theme setup
ctk.set_appearance_mode("system")  # "dark" or "light" or "system"
ctk.set_default_color_theme("dark-blue")  # Professional color theme

class PDFMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("✨ PDF Merger App")
        self.geometry("500x400")
        self.resizable(False, False)

        self.pdf_files = []
        self.merged_path = ""

        # Title Label
        title = ctk.CTkLabel(self, text="📄 Merge Your PDFs", font=("Arial", 24, "bold"), text_color="#1E88E5")
        title.pack(pady=20)

        # Upload Buttons
        self.btn_upload1 = ctk.CTkButton(self, text="📂 Upload First PDF", command=self.upload_pdf1, width=220,
                                         fg_color="#1976D2", hover_color="#1565C0", text_color="white")
        self.btn_upload1.pack(pady=10)

        self.btn_upload2 = ctk.CTkButton(self, text="📂 Upload Second PDF", command=self.upload_pdf2, width=220,
                                         fg_color="#1976D2", hover_color="#1565C0", text_color="white", state="disabled")
        self.btn_upload2.pack(pady=10)

        # Merge Button
        self.btn_merge = ctk.CTkButton(self, text="🔗 Merge PDFs", command=self.merge_pdfs,
                                       fg_color="#43A047", hover_color="#388E3C", text_color="white", width=220, state="disabled")
        self.btn_merge.pack(pady=15)

        # Save Button
        self.btn_save = ctk.CTkButton(self, text="💾 Save Merged PDF", command=self.save_pdf,
                                      fg_color="#0288D1", hover_color="#0277BD", text_color="white", width=220, state="disabled")
        self.btn_save.pack(pady=10)

        # Open Button
        self.btn_open = ctk.CTkButton(self, text="📖 Open PDF", command=self.open_pdf,
                                      fg_color="#F57C00", hover_color="#EF6C00", text_color="white", width=220, state="disabled")
        self.btn_open.pack(pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(self, text="No PDF uploaded yet.", text_color="#757575")
        self.status_label.pack(pady=10)

    # -----------------------------
    # Popup Notification (Fixed size, no close button)
    # -----------------------------
    def show_popup(self, message):
        popup = ctk.CTkToplevel(self)
        popup.title("Notification")
        popup.geometry("280x100")
        popup.resizable(False, False)
        popup.attributes("-topmost", True)
        popup.configure(fg_color="#424242")  # Dark background for popup

        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14, "bold"), wraplength=250, text_color="#FFFFFF")
        label.pack(expand=True, pady=20, padx=15)

        # Center popup on main window        popup.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2 - popup.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2 - popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")

    # -----------------------------
    # Upload PDF 1
    # -----------------------------
    def upload_pdf1(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file:
            self.pdf_files = [file]
            self.status_label.configure(text=f"✅ PDF 1 Uploaded: {os.path.basename(file)}")
            self.btn_upload2.configure(state="normal")
            self.show_popup("📄 First PDF uploaded successfully!")

    # -----------------------------
    # Upload PDF 2
    # -----------------------------
    def upload_pdf2(self):
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file:
            self.pdf_files.append(file)
            self.status_label.configure(text=f"✅ PDF 2 Uploaded: {os.path.basename(file)}")
            self.btn_merge.configure(state="normal")
            self.show_popup("📄 Second PDF uploaded successfully!")

    # -----------------------------
    # Merge PDFs (No Auto Save)
    # -----------------------------
    def merge_pdfs(self):
        if len(self.pdf_files) < 2:
            return  # No warning
        merger = PdfMerger()
        for pdf in self.pdf_files:
            merger.append(pdf)

        self.merged_path = "merged_output.pdf"
        merger.write(self.merged_path)
        merger.close()

        self.status_label.configure(text="🎉 PDFs merged successfully!")
        self.btn_save.configure(state="normal")
        self.btn_open.configure(state="normal")
        self.show_popup("🎉 PDFs merged successfully!")

    # -----------------------------
    # Save Merged PDF
    # -----------------------------
    def save_pdf(self):
        if not self.merged_path or not os.path.exists(self.merged_path):
            return  # No warning

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 title="Save merged PDF as")
        if save_path:
            os.replace(self.merged_path, save_path)
            self.merged_path = save_path
            self.status_label.configure(text=f"💾 Saved as {os.path.basename(save_path)}")
            self.show_popup("💾 File saved successfully!")

    # -----------------------------
    # Open PDF
    # -----------------------------
    def open_pdf(self):
        if not self.merged_path or not os.path.exists(self.merged_path):
            return  # No warning or notification
        webbrowser.open(self.merged_path)
        # No popup

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()
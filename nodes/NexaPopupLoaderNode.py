import tkinter as tk
# Assume tkinterdnd2 is installed for drag drop
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    TkinterDnD = tk
    DND_FILES = None

class NexaPopupLoaderNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {} }

    RETURN_TYPES = ()
    FUNCTION = "load"
    CATEGORY = "nexa"
    OUTPUT_NODE = True

    def load(self):
        # Create pop-up window for drag & drop model loading
        root = TkinterDnD.Tk() if TkinterDnD != tk else tk.Tk()
        root.title("Nexa Model Loader")
        root.geometry("400x200")

        label = tk.Label(root, text="Drag and drop Nexa model files here to load")
        label.pack(expand=True)

        loaded_files = []

        def on_drop(event):
            if DND_FILES:
                files = root.splitlist(event.data)
                for file in files:
                    loaded_files.append(file)
                    print(f"Loaded model: {file}")
                label.config(text=f"Loaded {len(loaded_files)} models")
            else:
                label.config(text="Drag & drop not supported, install tkinterdnd2")

        if DND_FILES:
            label.drop_target_register(DND_FILES)
            label.dnd_bind('<<Drop>>', on_drop)

        # Close button
        close_btn = tk.Button(root, text="Close", command=root.destroy)
        close_btn.pack()

        root.mainloop()
        return ()
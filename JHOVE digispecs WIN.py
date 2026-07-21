import os
import csv
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import PurePath


def process_xml(xml_file, output_csv):
    # JHOVE namespace
    ns = {
        "jhove": "http://schema.openpreservation.org/ois/xml/ns/jhove",
        "mix": "http://www.loc.gov/mix/v20"
    }

    tree = ET.parse(xml_file)
    root = tree.getroot()

    rows = []

    # Loop through each repInfo record
    for rep in root.findall("jhove:repInfo", ns):

        # URI and filename
        uri = rep.get("uri", "")
        filename = PurePath(unquote(uri)).name

        # Filesize
        size_elem = rep.find("jhove:size", ns)
        size = size_elem.text if size_elem is not None else ""

        # MD5 checksum
        md5 = ""
        checksums = rep.find("jhove:checksums", ns)

        if checksums is not None:
            for checksum in checksums.findall("jhove:checksum", ns):
                if checksum.get("type") == "MD5":
                    md5 = checksum.text
                    break

        # Width and Height
        width_elem = rep.find(".//mix:imageWidth", ns)
        height_elem = rep.find(".//mix:imageHeight", ns)

        width = width_elem.text if width_elem is not None else ""
        height = height_elem.text if height_elem is not None else ""

        # Status
        status_elem = rep.find("jhove:status", ns)
        status = status_elem.text.strip() if status_elem is not None and status_elem.text else ""

        # Messages
        message_elems = rep.findall("jhove:messages/jhove:message", ns)
        message = "; ".join(
            m.text.strip()
            for m in message_elems
            if m.text
        )

        rows.append([
            filename,
            size,
            width,
            height,
            md5,
            status,
            message
        ])

    # Write CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Filename",
            "Size",
            "ImageWidth",
            "ImageHeight",
            "MD5",
            "Status",
            "Messages"
        ])
        writer.writerows(rows)

    return (rows)


def browse_input():
    filename = filedialog.askopenfilename(
        title="Select XML File",
        filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
    )
    if filename:
        input_var.set(filename)


def browse_output():
    filename = filedialog.asksaveasfilename(
        title="Save CSV As",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if filename:
        output_var.set(filename)


def run_process():
    xml_file = input_var.get().strip()
    output_csv = output_var.get().strip()

    if not xml_file:
        messagebox.showerror("Error", "Please select an XML file.")
        return

    if not output_csv:
        messagebox.showerror("Error", "Please select an output CSV file.")
        return

    try:
        rows = process_xml(xml_file, output_csv)

        # Clear previous results
        results_box.delete("1.0", tk.END)

        # Equivalent of your first print block
        results_box.insert(
            tk.END,
            f"Extracted {len(rows)} records:\n\n"
        )

        for filename, size, width, height, md5, _, _ in rows:
            display_name = os.path.splitext(filename)[0]
            
            results_box.insert(
                tk.END,
                f"{display_name}: {size} bytes, "
                f"{width} x {height}, "
                f"MD5: {md5};\n"
            )

        results_box.insert(tk.END, "\nStatus Messages\n")
        results_box.insert(tk.END, "-" * 50 + "\n")

        # Equivalent of your second print block
        for filename, _, _, _, _, status, message in rows:
            display_name = os.path.splitext(filename)[0]
            
            results_box.insert(
                tk.END,
                f"{display_name}: {status}; {message}\n"
            )

        messagebox.showinfo(
            "Complete",
            f"Successfully extracted {len(rows)} records."
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
root = tk.Tk()
root.title("JHOVE XML to CSV & Digispecs")
root.geometry("850x530")
root.resizable(False, False)

input_var = tk.StringVar()
output_var = tk.StringVar()

# Input XML
tk.Label(root, text="Input XML:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=input_var, width=55).grid(row=0, column=1, padx=5)
tk.Button(root, text="Browse", command=browse_input).grid(row=0, column=2, padx=10)

# Output CSV
tk.Label(root, text="Output CSV:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=output_var, width=55).grid(row=1, column=1, padx=5)
tk.Button(root, text="Browse", command=browse_output).grid(row=1, column=2, padx=10)

# Run button
tk.Button(
    root,
    text="Extract",
    command=run_process,
    width=20,
    height=2
).grid(row=2, column=1, pady=20)

# Results window
results_box = scrolledtext.ScrolledText(
    root,
    width=100,
    height=20,
    wrap=tk.WORD
)
results_box.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
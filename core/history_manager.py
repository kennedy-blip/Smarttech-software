from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

class RepairHistory:
    def __init__(self, history_dir="logs/reports"):
        self.history_dir = history_dir
        # Ensure the directory exists so we don't get FileNotFoundError
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
        
        # Professional Shop Pricing (Adjust these values as you like)
        self.price_list = {
            "Security Scan": 15.00,
            "System Deep Clean": 10.00,
            "Factory Reset": 25.00,
            "System Update": 5.00,
            "Hardware Diagnostic": 10.00
        }

    def generate_pdf_report(self, device_id, actions_taken):
        """Creates a professional repair certificate and invoice PDF."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"{self.history_dir}/Invoice_{device_id}_{timestamp}.pdf"
        
        # Create the PDF object
        c = canvas.Canvas(filename, pagesize=A4)
        total_cost = 0.0
        
        # --- Header Section ---
        c.setFont("Helvetica-Bold", 20)
        c.setFillColorRGB(0.2, 0.4, 0.7)  # Professional Blue
        c.drawString(50, 800, "SMARTTECH REPAIR INVOICE")
        
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0, 0, 0) # Black text
        c.drawString(50, 780, f"Date: {datetime.now().strftime('%B %d, %Y')}")
        c.drawString(50, 765, f"Device Serial: {device_id}")
        c.line(50, 755, 550, 755)

        # --- Table Headers ---
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, 730, "Service Description")
        c.drawString(450, 730, "Price")
        c.line(50, 725, 550, 725)

        # --- List Items ---
        c.setFont("Helvetica", 11)
        y_pos = 705
        
        if not actions_taken:
            c.drawString(70, y_pos, "General Inspection / Consultation")
            c.drawString(450, y_pos, "$0.00")
            y_pos -= 20
        else:
            for action in actions_taken:
                # Logic to find the price based on the action name
                item_price = 0.0
                for key in self.price_list:
                    if key.lower() in action.lower():
                        item_price = self.price_list[key]
                        break
                
                c.drawString(70, y_pos, f"• {action}")
                c.drawString(450, y_pos, f"${item_price:.2f}")
                total_cost += item_price
                y_pos -= 20
                
                # Prevent text from going off the bottom of the page
                if y_pos < 150:
                    c.showPage()
                    y_pos = 800

        # --- Totals Section ---
        y_pos -= 20
        c.line(50, y_pos, 550, y_pos)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(340, y_pos - 30, f"TOTAL AMOUNT: ${total_cost:.2f}")
        
        # --- Footer ---
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(50, 80, "This document serves as a digital health certificate for the mentioned device.")
        c.drawString(50, 68, "All software optimizations are performed via SmartTech Pro Repair Suite.")
        c.drawString(50, 56, "Thank you for your business!")
        
        c.save()
        return filename
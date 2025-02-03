import matplotlib.pyplot as plt 
import shutil
import os

from reportlab.pdfgen import canvas 
from reportlab.lib.units import inch 



def send_email():
    pass

def generate_pdf_report():
    # Create a figure and axes for the plot 
    fig, ax = plt.subplots() 

    # Sample data 
    x = [1, 2, 3, 4, 5] 
    y = [10, 15, 7, 12, 9] 

    # Plot the line graph 
    ax.plot(x, y) 

    base_path = '/report'
    if not os.path.exists(base_path):
        os.makedir(base_path)

    # Save the plot as an image 
    tmp_path = base_path + '/tmp'
    os.makedirs(tmp_path, exist_ok=True)

    line_graph_png_path = tmp_path + '/line_graph.png'
    plt.savefig(line_graph_png_path) 

    # Create a PDF file 
    report_full_path = base_path + '/line_graph.pdf'
    c = canvas.Canvas(report_full_path) 

    # Add the image to the PDF 
    c.drawImage(line_graph_png_path, 1*inch, 4*inch, width=4*inch, height=3*inch) 

    # Save the PDF file 
    c.save() 

    # remove the tmp dir
    shutil.rmtree(tmp_path)
    

def generate_med_readiness_line_chart():
    pass

def generate_deployability_line_chart():
    pass

def generate_hello_world_line_chart() -> str:
    # Create a figure and axes for the plot 
    fig, ax = plt.subplots() 

    # Sample data 
    x = [1, 2, 3, 4, 5] 
    y = [10, 15, 7, 12, 9] 

    # Plot the line graph 
    ax.plot(x, y) 

    base_path = '/report'
    if not os.path.exists(base_path):
        os.makedir(base_path)

    # Save the plot as an image 
    tmp_path = base_path + '/tmp'
    os.makedirs(tmp_path, exist_ok=True)

    line_graph_png_path = tmp_path + '/line_graph.png'
    plt.savefig(line_graph_png_path) 
    return line_graph_png_path
    


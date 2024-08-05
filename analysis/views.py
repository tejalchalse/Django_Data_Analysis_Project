import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def upload_file(request):
    if request.method == 'POST' and request.FILES['my_file']:
        uploaded_file = request.FILES['my_file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        try:
            # Try reading the CSV file with different encodings
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='ISO-8859-1')
            
            # Perform analysis
            analysis = {
                'head': df.head().to_html(),
                'description': df.describe().to_html(),
                'missing_values': df.isnull().sum().to_frame(name='missing_values').to_html()
            }
            
            # Generate histogram
            plt.figure(figsize=(10, 6))
            df.hist(bins=30, figsize=(15, 10), layout=(5, 3))
            plt.tight_layout()
            
            # Save plot to a string in base64 format
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            plot_url = base64.b64encode(image_png).decode('utf-8')
            plot_url = 'data:image/png;base64,' + plot_url

        finally:
            # Delete the file after processing
            fs.delete(filename)
        
        return render(request, 'upload.html', {'analysis': analysis, 'plot_url': plot_url})
    
    return render(request, 'upload.html')

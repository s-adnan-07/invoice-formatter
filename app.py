from flask import Flask, render_template, request, send_file
from pypdf import PdfWriter, PdfReader
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      return 'No file uploaded', 400

    file = request.files['file']

    if file.filename == '':
      return 'No file selected', 400
    
    if not file.filename.endswith('.pdf'):
      return 'Please upload valid pdf file', 400

    if file:
      overlay = PdfReader('overlay.pdf').pages[0]
      overlay.transfer_rotation_to_content()
      filename = file.filename.removesuffix('.pdf')

      input_file = PdfWriter(clone_from=file.stream)
      output_file = BytesIO()

      for page in input_file.pages:
        page.merge_page(overlay, over=False)

      input_file.write_stream(output_file)
      output_file.seek(0)

      return send_file(output_file, mimetype='application/pdf', as_attachment=True, download_name=f"{filename}-final.pdf")

  return render_template('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5100)
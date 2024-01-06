from flask import Flask, render_template, request, redirect, url_for, send_file
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from io import BytesIO
import os
# rest of the code remains the same

app = Flask(__name__)

# Replace with your Azure Storage connection string and container name

connection_string = os.environ['connection_string_key']
container_name = "productpic"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(
    connection_string)
container_client = blob_service_client.get_container_client(container_name)


@app.route('/')
def index():
  # List blobs in the container
  blobs = [blob.name for blob in container_client.list_blobs()]

  return render_template('index.html', blobs=blobs)


@app.route('/view/<blob_name>')
def view_image(blob_name):
  # Do any additional processing if needed
  blob = container_client.get_blob_client(blob_name)
  blob_data = blob.download_blob().readall()

  # Wrap the bytes data in a BytesIO object
  bytes_io = BytesIO(blob_data)

  return send_file(bytes_io, mimetype='image/png')


@app.route('/upload', methods=['POST'])
def upload_file():
  if 'file' not in request.files:
    return redirect(request.url)

  file = request.files['file']

  if file.filename == '':
    return redirect(request.url)

  # Upload the file to the blob storage
  blob_client = container_client.get_blob_client(file.filename)
  blob_client.upload_blob(file)

  return redirect(url_for('index'))


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')

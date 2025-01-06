import React, { useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist/webpack';
import './upload.css';

const PdfUploader = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');

  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    if (file && file.type === 'application/pdf') {
      const fileReader = new FileReader();
      fileReader.onload = async function () {
        const typedarray = new Uint8Array(this.result);

        const pdf = await pdfjsLib.getDocument(typedarray).promise;

        if (pdf.numPages > 2) {
          alert('Please upload a PDF with a maximum of 2 pages.');
          return;
        }

        let extractedText = '';

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
          const page = await pdf.getPage(pageNum);
          const textContent = await page.getTextContent();
          const pageText = textContent.items.map((item) => item.str).join(' ');
          extractedText += pageText + ' ';
        }

        // Send extracted text to backend for storing
        handleSubmitPdf(file.name, extractedText);
      };
      fileReader.readAsArrayBuffer(file);
    } else {
      alert('Please select a valid PDF file.');
    }
  };

  const handleSubmitPdf = async (fileName, extractedText) => {
    setIsProcessing(true);
    setUploadMessage('Uploading PDF, please wait...');

    try {
      const storeResponse = await fetch('http://127.0.0.1:8000/api/store-pdf/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pdf_name: fileName, pdf_text: extractedText }),
      });

      if (!storeResponse.ok) {
        const errorData = await storeResponse.json();
        setUploadMessage(`Error: ${errorData.error}`);
      } else {
        setUploadMessage('PDF uploaded successfully. You can now continue to submit job links.');
      }
    } catch (error) {
      console.error('Network error:', error);
      setUploadMessage('Network error: Could not upload the PDF.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="pdf-uploader">
      <h2 className="pdf-uploader-title">Upload Your Resume (PDF, Max 2 Pages)</h2>
      <input
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        className="pdf-uploader-input"
      />
      {uploadMessage && (
        <div className="pdf-upload-message">
          <p>{uploadMessage}</p>
        </div>
      )}
    </div>
  );
};

export default PdfUploader;

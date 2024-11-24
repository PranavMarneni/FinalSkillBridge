import React, { useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist/webpack';
import './upload.css'; // Import CSS file

const PdfUploader = () => {
  const [text, setText] = useState('');

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

        setText(extractedText);
      };
      fileReader.readAsArrayBuffer(file);
    } else {
      alert('Please select a valid PDF file.');
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
      {text && (
        <div className="pdf-uploader-result">
          <h3 className="pdf-uploader-result-title">Extracted Text:</h3>
          <pre className="pdf-uploader-result-text">{text}</pre>
        </div>
      )}
    </div>
  );
};

export default PdfUploader;

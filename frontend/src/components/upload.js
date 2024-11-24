import React,{useState} from "react";
import {useDropzone} from "react-dropzone";
import * as pdfjsLib from "pdfjs-dist";

/*PDF.js uses external processor*/
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

/*
  Explanation of useState and [variable, variable] Syntax in React:

  React provides the `useState` Hook to add state to functional components. 
  The syntax `const [stateVariable, setStateFunction] = useState(initialValue)` 
  is commonly used for this purpose.

  1. What is happening here?
     - `useState(initialValue)`:
       - This initializes a piece of state with the provided `initialValue`. 
       - It returns an array with two elements:
         - The **current state value**.
         - A **function to update the state**.

     - `[stateVariable, setStateFunction]`:
       - The array returned by `useState` is **destructured** into two variables:
         - `stateVariable`: Holds the current value of the state.
         - `setStateFunction`: A function used to update the state value.

  2. Example:
     ```javascript
     const [count, setCount] = useState(0);
     ```
     - `count`: The current state value, initialized to `0`.
     - `setCount`: A function to update `count`.

     Usage:
     ```javascript
     <button onClick={() => setCount(count + 1)}>
       Increment Count: {count}
     </button>
     ```
     - When `setCount` is called, React updates the state, and the component re-renders.

  3. Practical Example from this Component:
     ```javascript
     const [text, setText] = useState("");      // `text` stores extracted text
     const [loading, setLoading] = useState(false); // `loading` tracks processing state
     ```
     - `text` starts as an empty string and can be updated with `setText(newText)`.
     - `loading` starts as `false` and can be updated with `setLoading(true/false)`.

     These states could be used as follows:
     ```javascript
     if (loading) {
       return <div>Loading...</div>;
     }

     return <div>Extracted Text: {text}</div>;
     ```

  4. Why use this syntax?
     - **Declarative State Management**:
       - The `useState` Hook lets you define and manage state in a readable, structured way.
     - **Reactivity**:
       - When you update state using `setStateFunction`, React automatically re-renders the component to reflect the latest state in the UI.
     - **Encapsulation**:
       - Each piece of state is managed independently, improving modularity and readability.

  5. Key Notes:
     - React functional components **must re-render** to reflect state changes.
     - `setStateFunction` triggers a re-render, and the state variable (`stateVariable`) will contain the updated value in the next render.

  Summary:
  - The `[stateVariable, setStateFunction] = useState(initialValue)` pattern is a clean, declarative way to manage state in React functional components.
  - It ensures the UI stays in sync with the underlying state.
  - In this component, `text` and `loading` are independent states, managed using `setText` and `setLoading` respectively.
*/



{/*Create function for PDFextraction
    -useState is used to manage the component's state*/}



const PdfExtractor = () => {
    {/* initialize variable text with empty string
        Settext is a function used to update state
        */}
    const[text,setText] = useState("");
    const [loading,setLoading] = useState(false);

    const onDrop = async (acceptedFiles) => {
        const file = acceptedFiles[0];
        if (file && file.type === "application/pdf") {
          setLoading(true);
          const text = await extractTextFromPdf(file);
          setText(text);
          setLoading(false);
        } else {
          alert("Please upload a valid PDF file.");
        }
      };

      const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: "application/pdf",
      });
      const extractTextFromPdf = async (file) => {
        const arrayBuffer = await file.arrayBuffer();
        const pdfDoc = await pdfjsLib.getDocument(arrayBuffer).promise;
    
        let extractedText = "";
        for (let i = 1; i <= pdfDoc.numPages; i++) {
          const page = await pdfDoc.getPage(i);
          const content = await page.getTextContent();
          const pageText = content.items.map((item) => item.str).join(" ");
          extractedText += `\n${pageText}`;
        }
    
        return extractedText;
      };
      return (
        <div style={{ padding: "20px", border: "1px solid #ccc", textAlign: "center" }}>
          <div
            {...getRootProps()}
            style={{
              border: "2px dashed #ccc",
              borderRadius: "10px",
              padding: "20px",
              cursor: "pointer",
            }}
          >
            <input {...getInputProps()} />
            <p>Drag and drop a PDF here, or click to select a file</p>
          </div>
    
          {loading ? (
            <p>Extracting text, please wait...</p>
          ) : text ? (
            <div style={{ marginTop: "20px", textAlign: "left" }}>
              <h3>Extracted Text:</h3>
              <pre style={{ whiteSpace: "pre-wrap" }}>{text}</pre>
            </div>
          ) : null}
        </div>
      );
    };
    
    export default PdfExtractor;
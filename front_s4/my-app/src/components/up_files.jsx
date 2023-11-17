import React, { useState } from "react";
import axios from "axios";

const CsvViewer = () => {
  const [csvData, setCsvData] = useState([]);
  const [header, setHeader] = useState([]);
  const [fileLoaded, setFileLoaded] = useState(false);
  const [isCsv, setIsCsv] = useState(false); // Adicione um estado para verificar se o arquivo é CSV
  const maxRowsToShow = 3;

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (file) {
      const fileName = file.name.toLowerCase();
      if (fileName.endsWith(".parquet")) {
        setFileLoaded(true);
        setIsCsv(false); // Define isCsv como falso para arquivos Parquet
      } else if (fileName.endsWith(".csv")) {
        const reader = new FileReader();
        reader.onload = (event) => {
          const text = event.target.result;
          const rows = text.split("\n").map((row) => row.split(","));
          setHeader(rows[0]);
          setCsvData(rows.slice(1, maxRowsToShow + 1));
          setFileLoaded(true);
          setIsCsv(true); // Define isCsv como verdadeiro para arquivos CSV
        };
        reader.readAsText(file);
      }
    } else {
      alert("Por favor, selecione um arquivo.");
    }
  };

  const handleSendClick = async () => {
    if (!fileLoaded) {
      alert("Por favor, selecione um arquivo antes de enviar.");
      return;
    }

    // Aqui você pode verificar o estado de isCsv
    if (setFileLoaded) {
      // Se é um arquivo CSV, você pode prosseguir com o envio
      const serverUrl = "http://3.93.70.161/uploadfile"; // Substitua pela URL do servidor EC2

      try {
        const formData = new FormData();
        formData.append("file", document.getElementById("csvFile").files[0]); // Use 'file' como nome do campo

        const response = await axios.post(serverUrl, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        console.log("Resposta do servidor:", response.data);

        // Limpe o estado ou realize qualquer ação adicional após o envio
        // ...

        alert("Arquivo enviado com sucesso!");
      } catch (error) {
        console.error("Erro ao enviar o arquivo:", error);
        alert("Erro ao enviar o arquivo. Por favor, tente novamente.");
      }
    }
  };

  return (
    <div className="h-screen flex flex-col items-center justify-center">
      <h1 className="mb-40 text-3xl font-bold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl justify-center flex mt-10 ">
        Visualizador de arquivo
      </h1>
      <div
        className={`bg-white p-8 rounded ${
          fileLoaded ? "" : "shadow-xl"
        } w-96 flex flex-col items-center justify-center h-auto`}
      >
        <div className="mb-4">
          <label className="flex text-gray-700 text-sm font-bold mb-2 justify-center">
            Selecione um arquivo CSV ou Parquet:
          </label>
          <input
            type="file"
            accept=".csv, .parquet"
            onChange={handleFileChange}
            className="w-full border rounded py-2 px-3 text-gray-700 focus:outline-none focus:shadow-outline"
            id="csvFile"
          />
        </div>
        {fileLoaded && (
          <>
            <table className={`table-auto w-full ${isCsv ? "" : "hidden"}`}>
              <thead>
                <tr>
                  {header.map((col, index) => (
                    <th key={index} className="border px-4 py-2">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {csvData.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                      <td key={cellIndex} className="border px-4 py-2">
                        {cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
            <div>
              <button
                onClick={handleSendClick}
                className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              >
                Enviar
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default CsvViewer;

import React, { useState, type ChangeEvent } from 'react';

interface UploadStatus {
  message: string;
  isError: boolean;
}

const ExcelUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [status, setStatus] = useState<UploadStatus | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      
      // Basic validation for Excel files
      if (selectedFile.type !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
        setStatus({ message: 'Please select a valid .xlsx file', isError: true });
        return;
      }

      setFile(selectedFile);
      setStatus(null);
    }
  };

  const handleUpload = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setStatus(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/uploads/submit-excel', {
        method: 'POST',
        body: formData,
        // Note: Don't set 'Content-Type' header; 
        // the browser will automatically set it to multipart/form-data with the boundary.
      });

      if (!response.ok) throw new Error('Upload failed');

      const data = await response.json();
      setStatus({ message: 'File uploaded successfully!', isError: false });
      setFile(null); // Reset input
    } catch (error) {
      setStatus({ message: 'Error uploading file. Please try again.', isError: true });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-sm bg-white">
      <h3 className="text-lg font-semibold mb-4">Upload Spoor Data (.xlsx)</h3>
      
      <form onSubmit={handleUpload} className="space-y-4">
        <input
          type="file"
          accept=".xlsx"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100"
        />

        <button
          type="submit"
          disabled={!file || uploading}
          className={`px-4 py-2 rounded font-bold text-white transition-colors
            ${!file || uploading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
        >
          {uploading ? 'Uploading...' : 'Upload Excel'}
        </button>
      </form>

      {status && (
        <p className={`mt-4 text-sm ${status.isError ? 'text-red-600' : 'text-green-600'}`}>
          {status.message}
        </p>
      )}
    </div>
  );
};

export default ExcelUpload;
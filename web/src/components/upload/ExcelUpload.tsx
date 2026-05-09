import React, { useState, type ChangeEvent } from 'react';
import styles from './ExcelUpload.module.css';

interface UploadStatus {
  message: string;
  isError: boolean;
}

interface UploadResponse {
  status: string;
  message: string;
  geocodenaam: string;
}

const ExcelUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [data, setData] = useState<UploadResponse | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [status, setStatus] = useState<UploadStatus | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
        setStatus({ message: 'Please select a valid .xlsx file', isError: true });
        return;
      }
      setFile(selectedFile);
      setStatus(null);
    }
  };

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
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
      });

      if (!response.ok) throw new Error('Upload failed');

      const response_data: UploadResponse = await response.json();
      setStatus({ message: 'File uploaded successfully!', isError: false });
      setFile(null);
      setData(response_data)
    } catch (error) {
      setStatus({ message: 'Error uploading file. Please try again.', isError: true });
      setData({ message: 'Error uploading file. Please try again.', status: "failed", geocodenaam: "onbekend"});
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Upload Spoor Data (.xlsx)</h3>
      <form onSubmit={handleUpload} className={styles.form}>
        <input
          type="file"
          accept=".xlsx"
          onChange={handleFileChange}
          className={styles.fileInput}
        />
        <button
          type="submit"
          disabled={!file || uploading}
          className={styles.button}
        >
          {uploading ? 'Uploading...' : 'Upload Excel'}
        </button>
      </form>
      {status && (
        <p className={`${styles.statusMessage} ${status.isError ? styles.error : styles.success}`}>
          {data?.geocodenaam || status.message}
        </p>
      )}
    </div>
  );
};

export default ExcelUpload;

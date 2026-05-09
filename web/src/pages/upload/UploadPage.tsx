import React from 'react';
import ExcelUpload from "../../components/upload/ExcelUpload";
import styles from './UploadPage.module.css'; // Import the styles

const UploadPage: React.FC = () => {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Data Import</h1>
        <p className={styles.description}>
          Upload your Excel files here to synchronize the Spoor data with the database.
        </p>
      </header>

      <div className={styles.layoutGrid}>
        {/* Main Upload Section */}
        <div className={styles.mainContent}>
          <ExcelUpload />
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
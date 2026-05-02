import React from 'react';
import ExcelUpload from "../../components/upload/ExcelUpload";

const UploadPage: React.FC = () => {
  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Data Import</h1>
        <p className="mt-2 text-gray-600">
          Upload your Excel files here to synchronize the Spoor data with the database.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Main Upload Section */}
        <div className="md:col-span-2">
          <ExcelUpload />
        </div>

        {/* Requirements/Sidebar Section */}
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
          <h2 className="text-sm font-bold text-blue-800 uppercase tracking-wider mb-3">
            Requirements
          </h2>
          <ul className="text-sm text-blue-700 space-y-2 list-disc list-inside">
            <li>File must be in <strong>.xlsx</strong> format.</li>
            <li>Ensure the "ID" column is present.</li>
            <li>Maximum file size: 10MB.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
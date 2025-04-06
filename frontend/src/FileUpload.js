import React, { useState } from "react";
import { UploadCloud, CheckCircle, XCircle } from "lucide-react";
import { useAuth0 } from "@auth0/auth0-react";  // Auth0 hook for authentication
import geminiicon from "../src/gemini_icon.png"

// RiskBarometer component to show the risk status visually
const RiskBarometer = ({ status }) => {
  const riskLevels = {
    low: { color: "green", label: "Low Risk" },
    medium: { color: "brown", label: "Medium Risk" },
    high: { color: "red", label: "High Risk" },
  };

  const risk = riskLevels[status.status] || { color: "gray", label: "No Risk" };

  return (
    <div className="risk-barometer">
      <div
        className="bar"
        style={{
          width: "100%",
          height: "20px",
          backgroundColor: "#ddd",
          borderRadius: "10px",
          marginBottom: "0px"
        }}
      >
        <div
          style={{
            width: status.status === "low" ? "33%" : status.status === "medium" ? "66%" : "100%",
            height: "100%",
            backgroundColor: risk.color,
            borderRadius: "10px",
          }}
        />
      </div>
      <p style={{ color: risk.color, textAlign: "center" }}>{risk.label}</p>
    </div>
  );
};

export default function FileUploadPage() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [randomStatus, setRandomStatus] = useState("");
  const [isFetchingStatus, setIsFetchingStatus] = useState(false);
  const [downloadEnabled, setDownloadEnabled] = useState(false);
  const [isPopupVisible, setIsPopupVisible] = useState(false);  // State to control popup visibility
  const { loginWithRedirect, logout, isAuthenticated, user, getAccessTokenSilently } = useAuth0();

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setUploadStatus(null);
    }
  };

  const generateReport = async () => {
    if (!file) {
      alert("Please upload a file before generating the report.");
      return;
    }
    try {
      // Call the backend to generate the report (Modify URL and logic accordingly)
      const response = await fetch("http://127.0.0.1:5000/generate-report", {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        alert("Report generated successfully!");
      } else {
        alert("Failed to generate the report.");
      }
    } catch (error) {
      alert("Error generating the report.");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      if (response.ok) {
        setUploadStatus("success");
      } else {
        setUploadStatus("error");
      }
    } catch (error) {
      setUploadStatus("error");
    } finally {
      setIsUploading(false);
    }
  };

  const getRandomStatus = async () => {
    setIsFetchingStatus(true);

    // Simulate a delay (e.g., 2 seconds)
    setTimeout(async() => {
      const randomStatus =  await fetch("http://127.0.0.1:5000/random-status", {
        method: "GET",
      });
      const result = await randomStatus.json();
      setRandomStatus(result);
      setDownloadEnabled(true);
      setIsFetchingStatus(false);
    }, 2000);
  };

  const handleDownload = async (event) => {
    event.preventDefault(); // Prevent the default behavior, which might cause a page reload
  
    // Check if user is authenticated
    if (!isAuthenticated) {
      loginWithRedirect();  // Redirect to login if not authenticated
      return;
    }
  
    try {
      // Get access token
      const token = await getAccessTokenSilently();
  
      // Fetch the file using the token
      const response = await fetch("http://127.0.0.1:5000/download", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "downloaded-file"; // Specify the download file name
        a.click();
        window.URL.revokeObjectURL(url);
      } else {
        alert("Download failed. Please try again.");
      }
    } catch (error) {
      alert("Error fetching the file.");
    }
  };
  return (
    <div className="file-upload-container">
      <div className="file-upload-card">
        <UploadCloud className="icon" />
        <h1>Upload your file</h1>
        <p>Drag & drop files here or click to select</p>
        <label className="file-input-label">
          <input type="file" onChange={handleFileChange} className="file-input" />
          <div className="file-input-box">
            {file ? (
              <span>{file.name}</span>
            ) : (
              <span>Click to select a file</span>
            )}
          </div>
        </label>
        <button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className="upload-btn"
        >
          {isUploading ? (
            <div className="loader"></div>
          ) : (
            "Upload"
          )}
        </button>
        <br />
        {uploadStatus === "success" && !isUploading && (
          <div className="status success">
            <CheckCircle className="status-icon" /> Upload successful!
          </div>
        )}
        {uploadStatus === "error" && !isUploading && (
          <div className="status error">
            <XCircle className="status-icon" /> Upload failed. Try again.
          </div>
        )}

        <button
          onClick={getRandomStatus}
          className="random-status-btn"
          disabled={isFetchingStatus || uploadStatus !== "success"}
        >
          {isFetchingStatus ? (
            <div className="loader"></div> // Show loader
          ) : (
            "Get Risk Levels Assessed"
          )}
        </button>

        {randomStatus && (
          <div className="random-status">
            <span className="status-text">Risk Level</span>
          </div>
        )}

        {randomStatus && <RiskBarometer status={randomStatus} />}
        <br />

       {/* Gemini Report Button */}
<button
  onClick={generateReport}
  className="generate-report-btn"
  disabled={!file || isUploading}
>
  Generate Report with Gemini
</button>
        
        <br />

{/* Login/Download Button — now below the Gemini button */}
<button
  onClick={handleDownload}
  className="download-btn"
  disabled={!downloadEnabled}
>
  {isAuthenticated ? "Download File" : "Please Log In to Download"}
</button>

        {isPopupVisible && isAuthenticated && (
          <div className="popup">
            <div className="popup-content">
              <h3>User Details</h3>
              <p><strong>Name:</strong> {user.name}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Nickname:</strong> {user.nickname}</p>
              <button onClick={() => setIsPopupVisible(false)} className="close-btn">Close</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

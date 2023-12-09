import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";

import "./style.css";

function CaptureForm() {
  const [start, setStart] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [rollno, setRollno] = useState("");
  const [images, setImages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (images.length !== 5) {
      return;
    }

    const folderPath = "images/";

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("rollno", rollno);
    images.forEach((image, index) => {
      formData.append(
        "images",
        dataURItoBlob(image),
        `${folderPath}${index}.jpg`
      );
    });

    try {
      await axios.post(process.env.REACT_APP_URL + "/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      alert("Data sent successfully");
    } catch (error) {
      console.error("Error sending data:", error);
      alert(error.message);
    } finally {
      setStart(false);
      setImages([]);
      setProgress(0);
      setName("");
      setEmail("");
      setRollno("");
    }
  };

  const dataURItoBlob = (dataURI) => {};

  return (
    <div className="">
      <form onSubmit={handleSubmit}>
        <div className="table-parent">
          <table className="form-table">
            <thead>
              <tr>
                <td>
                  <label>Name:</label>
                </td>
                <td>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </td>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <label>Email:</label>
                </td>
                <td>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <label>Roll No:</label>
                </td>
                <td>
                  <input
                    type="number"
                    value={rollno}
                    onChange={(e) => setRollno(e.target.value)}
                    required
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        {start ? (
          <div className="parent-camera">
            <div className="webcam-container">
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                mirrored={true}
                width={500}
                height={500}
              />

              <div>
                {images.length === 5 ? (
                  <button className="btn" type="submit">
                    Submit Form with Images
                  </button>
                ) : (
                  <button
                    className="btn"
                    onClick={captureImage}
                    disabled={images.length >= 5}
                  >
                    Capture Image ({images.length}/5)
                  </button>
                )}
              </div>
            </div>
            <div className="pics-1">
              <h1>Images Captured</h1>
              <div className="pics-2">
                {images &&
                  images.map((image, index) => (
                    <img
                      key={index}
                      src={image}
                      alt={`captured ${index + 1}`}
                      style={{ width: 100, height: 100 }}
                    />
                  ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="start-btn">
            <button className="btn" onClick={() => setStart(true)}>
              Start Camera
            </button>
          </div>
        )}
      </form>
    </div>
  );
}

export default CaptureForm;

import React, { useState, useRef } from "react";
import Webcam from "react-webcam";

import "./style.css";

function CaptureForm() {
  const handleSubmit = (e) => {};

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
                  <input type="text" required />
                </td>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <label>Email:</label>
                </td>
                <td>
                  <input type="email" required />
                </td>
              </tr>
              <tr>
                <td>
                  <label>Roll No:</label>
                </td>
                <td>
                  <input type="number" required />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </form>
    </div>
  );
}

export default CaptureForm;

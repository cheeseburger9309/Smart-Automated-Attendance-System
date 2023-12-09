import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <>
      <div>
        <Link to={"/"}>
          <div>
            <span>A</span>ttendance <span>T</span>racking <span>S</span>ystem
          </div>
        </Link>
        <ul>
          <li>
            <a href="/dashboard">Sheet</a>
          </li>
        </ul>
      </div>
    </>
  );
};

export default Header;

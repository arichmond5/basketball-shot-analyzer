import { Link } from "react-router-dom";
import logo from "../../assets/BasketballLogo.jpeg";
import "./Navbar.css";

function Navbar() {
  return (
    <nav>

      {/* Logo */}
      <div className="logo">
        <Link to="/">
          <img src={logo} alt="Logo" />
        </Link>
      </div>

      {/* Nav links */}
      <ul id="navbar">
        <li>
          <Link to="/">Home</Link>
        </li>

        <li>
          <Link to="/upload">Upload</Link>
        </li>
      </ul>

    </nav>
  );
}

export default Navbar;

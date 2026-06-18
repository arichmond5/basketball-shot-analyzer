import "./navbar.css"
import logo from "../assets/LEBRON.jpeg";

function Navbar() {
  return (
    <nav>
      <a href="#home" className="logo">
        <img src={logo} alt="Logo" />
      </a>

      <div>
        <ul id="navbar">
          <li>
            <a href="#home">Home</a>
          </li>

          <li>
            <a href="#how-it-works">How It Works</a>
          </li>

          <li>
            <a href="#results">Results</a>
          </li>

          <li>
            <a href="#about">About</a>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
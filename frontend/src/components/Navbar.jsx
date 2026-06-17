import "./navbar.css"
import logo from "../assets/LEBRON.jpeg";

function Navbar() {
  return (
    <>
      <nav>
        <a href="index.html" className="logo">
          <img src={logo} alt="Logo" />
        </a>

        <div>
          <ul id="navbar">
            <li>
              <a href="index.html">Home</a>
            </li>

            <li>
              <a href="index.html">How It Works</a>
            </li>

            <li>
              <a href="index.html">Results</a>
            </li>

            <li>
              <a href="index.html">About</a>
            </li>
          </ul>
        </div>
      </nav>
    </>
  );
}

export default Navbar;
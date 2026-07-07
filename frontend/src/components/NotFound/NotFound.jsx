import "./NotFound.css"

function NotFound() {
  return (
    <div className="not-found-page">

      <div className="not-found-content">
        <h1>404</h1>
        <h2>Page not found</h2>
        <p>
          The page you're looking for doesn't exist.
        </p>

        <a href="/">
          Return Home
        </a>
      </div>
    </div>
  );
}

export default NotFound;
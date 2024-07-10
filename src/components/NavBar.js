import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css'; // Import the CSS file

function NavBar() {
  return (
    <nav className="navbar">
      <ul className="navbar-list">
        <li className="navbar-item">
          <Link to="/" className="navbar-link">Home</Link>
        </li>
        <li className="navbar-item">
          <Link to="/movies" className="navbar-link">Movies</Link>
        </li>
        <li className="navbar-item">
          <Link to="/profile" className="navbar-link">Profile</Link>
        </li>
        <li className="navbar-item">
          <Link to="/reviews" className="navbar-link">Reviews</Link>
        </li>
      </ul>
    </nav>
  );
}

export default NavBar;

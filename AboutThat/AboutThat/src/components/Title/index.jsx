import React from "react";
import { Link } from "react-router-dom";
import styles from "./navbar.module.css";

//TODO Web Template Studio: Add a new link in the NavBar for your page here.
// A skip link is included as an accessibility best practice. For more information visit https://www.w3.org/WAI/WCAG21/Techniques/general/G1.
export default function Title() {
  return (
    <React.Fragment>
      <div className={styles.skipLink}>
        <a href="#mainContent">Skip to Main Content</a>
      </div>
      <nav className="navbar-brand" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    }}>
        <div style={{position: 'fixed', top: '0', left: '0',  width: '100%',  height: '88px',  zIndex: '10', background: '#eeeeee', textAlign: 'center'}}>
          <Link className="navbar-brand" to="/" style={{textAlign: 'center', padding: '15px 20px', fontSize: '36px', color: 'black', fontFamily: 'PT Sans Narrow'}}>
            About That
          </Link>
        </div>
      </nav>
    </React.Fragment>
  );
}

import React from "react";
import styles from "./footer.module.css";

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className="container-fluid">
        <div className="row justify-content-around">
          <div className="col-8 col-md-5">
            <h5 className={styles.title}>AboutThat</h5>
            <p className={styles.description}>
                  "About This" allows voters to search for words/phrases that matter to them and 
                  then view a bar graph showing them how much news bias there is on this topic. 
                  The bar graph compares several news sources and their sentiment of the searched word/phrase. 
                  {/* Note: data is self-generated, not accurate reflections of news sources yet.
                  Currently supported searchs: "Trump", "guns", "global warming", "taxes", 
                  "third party", "republican", "democrat", "government", "Hillary", "politics". */}
            </p>
          </div>
          <p style={{color: 'white'}}>Currently Supported News Platforms:</p>
          <div className="col-2">
            <ul className="list-unstyled">
              <li>
                <a className={styles.footerlink} href="https://www.cnn.com/">
                  CNN
                </a>
              </li>
              <li>
                <a className={styles.footerlink} href="https://www.fox.com/news/">
                  FOX
                </a>
              </li>
              <li>
                <a className={styles.footerlink} href="https://www.bbc.com/">
                  BBC
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}

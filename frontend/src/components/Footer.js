import styles from '../css/footer.module.css';

function Footer() {
    return(
        <div className={styles.div}>
        <a
          href="https://sanjivkannaa.github.io"
        >
          Built by Sanjiv Kannaa
        </a>
        |
        <a
          href="https://github.com/sanjivkannaa/chaosbank"
        >
          View on Github
        </a>
      </div>
    )
}

export default Footer;

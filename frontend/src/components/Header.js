import styles from '../css/header.module.css';
import appLogo from '../assets/AppLogoFull.png';

function Header() {
    return(
        <div className={styles.App}>
            <img 
                src={appLogo}
                alt="AppLogo"
                className={styles.appLogo}
            />
        </div>
    )
}

export default Header;
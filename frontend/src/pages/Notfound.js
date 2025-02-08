import logo from '../asserts/404_image.png';
import styles from '../css/notFound.module.css';

function Notfound() {
  return (
    <div className={styles.App}>
      <header className={styles.AppHeader}>
        <img src={logo} alt="logo" />
        <p>
          <br />
          Awwww...Dont Cry.
          <br />
          It's just a 404 Error! 
          <a className={styles.homePage} href='/'>Click here to get back to the home page</a>
        </p>
      </header>
    </div>
  );
}

export default Notfound;

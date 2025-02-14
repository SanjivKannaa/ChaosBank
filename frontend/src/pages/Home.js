import Header from "../components/Header";
import Footer from "../components/Footer";
import styles from '../css/home.module.css';
import AppName from "../assets/AppName.png"
import QuickLinks from "../components/QuickLinks";

function Home() {
  return (
    <div className={styles.App}>
      <QuickLinks />
      <Header />
      <br /><br /><br /><br />
      <div className={styles.div1}>
        <div className={styles.div11}>
          <h1>
            Welcome to
            <br />
            <img
              src={AppName}
              alt="ReliaBank"
            />
          </h1>
        </div>
        <div className={styles.div12}>
          <h1>
            A Secure and Reliable Banking Solution for the Modern World.
          </h1>
        </div>
      </div>

      <div className={styles.div2}>
        <br />
        <div className={styles.div21}>
          <h1>
            Why Reliabank?
          </h1>
        </div>
        <br />
        <div className={styles.div22}>
          <h1>
            Built a simple Banking Web Application, with a focus on:
          </h1>
          <ul>
            <h2><li>Application Security</li></h2>
            <h2><li>DevOps</li></h2>
            <h2><li>Scalability</li></h2>
            <h2><li>Chaos Engineering</li></h2>
          </ul>
        </div>
      </div>

      <div className={styles.div3}>
        <br />
        <div className={styles.div31}>
          <h1>
            Tech Stack
          </h1>
        </div>
        <br />
        <div className={styles.div32}>
          <div className={styles.div32a}>
            Frontend
            <ul>
              <li>React JS</li>
              <li>Material UI</li>
            </ul>
            Database
            <ul>
              <li>mySQL</li>
            </ul>
          </div>
          <div className={styles.div32b}>
            Backend
            <ul>
              <li>Flask</li>
              <li>JWT (auth)</li>
              <li>Bcrytp</li>
            </ul>
          </div>
          <div className={styles.div32c}>
            DevOps
            <ul>
              <li>Docker, docker-compose</li>
              <li>Gitlabs CI</li>
              <li>Jenkins CD</li>
              <li>Terraform, Ansible</li>
            </ul>
          </div>
          <div className={styles.div32d}>
            Deployment
            <ul>
              <li>AWS</li>
            </ul>
            Chaos Engineering
            <ul>
              <li>K6 load testing</li>
            </ul>
          </div>
        </div>
      </div>
      <Footer />

    </div>
  );
}

export default Home;

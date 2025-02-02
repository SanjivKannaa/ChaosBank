import logo from '../components/404_image.png';
import './css/global.css';

function Notfound() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="logo" />
        <p>
          <br />
          Awwww...Dont Cry.
          <br />
          It's just a 404 Error! 
          Click here to get back to the<a style={{ color: '#ff5733', fontWeight: 'bold', textDecoration: 'none', marginLeft: '5px' }} href='/'>home page</a>
        </p>
      </header>
    </div>
  );
}

export default Notfound;

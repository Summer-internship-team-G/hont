import React from 'react';
import { Link } from 'react-router-dom';
import hontLogo from '../images/Logo.png';
import axios from "axios";

export default () => {
  const [auth, setAuth] = useState("");

  useEffect(() => {
    if (localStorage.getItem('token') !== null){
      setAuth(true);
    }
    else {
      setAuth(false);
    }
  }, [])

  const handleLogout = async () => {
    const postUrl = "http://localhost:5000/auth/logout";
    const postVal = {
      quit: true,
    }
    await axios.post(postUrl, postVal, {
      headers: {
        'Content-type' : 'application/json',
        'Authorization' : `JWT ${localStorage.getItem("token")}`,
      }
    })
    .then((response) => {
      if(response.data.status == "success"){
        alert(response.data.message);
        localStorage.clear();
      }
      else{
        alert(response.data.message);
      }
    })
  }

  return (
    <header>
      <span><Link to='/'>
                <img src={hontLogo}/>
                <span>HONT</span>
            </Link>
      </span>
      <Link to='/signup'>Signup</Link>
      {auth ? 
                  <Link to='/' onClick={handleLogout}>Logout</Link>
                : 
                  <><Link to='/signup'>Signup</Link>
                  <Link to='/login'>Login</Link></>
              } 
    </header>
  )
}
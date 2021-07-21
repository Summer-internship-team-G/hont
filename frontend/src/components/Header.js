import React from 'react';
import { Link } from 'react-router-dom';
import Session from './SessionCheck';
import hontLogo from '../images/Logo.png';
import axios from "axios";

export default () => {
  const quitSession = async () => {
    const postUrl = "http://localhost:5000/user/signout";
    const postVal = {
      quit: true,
    }
    await axios.post(postUrl, postVal)
    .then((response) => {
      if(response.data.error == "true"){
        console.log("세션 없음");
      }
      else{
        console.log("세션 종료");
        alert("로그아웃 되었습니다.");
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
      {<Session/> ? 
                <Link to='/login'>Login</Link> : 
                <Link to='/' onClick={quitSession}>Logout</Link>
              } 
    </header>
  )
}
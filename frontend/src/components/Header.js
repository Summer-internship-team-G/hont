import React, { useState, useEffect } from 'react';
import { Link, withRouter } from 'react-router-dom';
import styled from "styled-components";
import { SVG1, SVG2 } from './SVG';
import hontLogo from '../image/Logo.png';
import axios from "axios";

const Logo = styled.span`
    color: #FFFFFF;
    font-size: 130px;
    margin-top: 20px;
    margin-left: 100px;
    display: flex;
`;

const Header = styled.header`
  font-family: "Baloo Bhaijaan", sans-serif;
  position: relative;
  width: 100%;
  font-weight: 600;
`;

const Nav = styled.span`
  color: #FFFFFF;
  font-size: 60px;
  margin-right: 100px;
`;

const Margin = styled.span`
  margin-right: 50px;
  margin-left: 50px;
`;

export default withRouter(({ location: { pathname }}) => {
  const isSVG2 =  pathname === "/" || 
                  pathname === "/login" ||
                  pathname === "/signup" || 
                  pathname === "/Result" ||
                  pathname === "/statistics";

  const useGetData = () => {
    const [auth, setAuth] = useState("");
    
    useEffect(() => {
      if (localStorage.getItem('token') !== null){
        setAuth(true);
      }
      else {
        setAuth(false);
      }
    }, [localStorage.getItem('token')])
    
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
          setAuth(false);
          localStorage.clear();
        }
        else{
          alert(response.data.message);
        }
      })
    }

    return {
      auth,
      handleLogout,
    }
  }

  const { auth, handleLogout } = useGetData();

  return(
    <Header className="headerContainer">
          {isSVG2 ? <SVG2/> : <SVG1/>}
          <div className="headerItem">
            <Logo>
              <Link to='/'>
                <img src={hontLogo} className="hontLogo"/>
                <span className="textShadow">HONT</span>
              </Link>
            </Logo>
          </div>
          <div className="headerItem">
            <Nav className="textShadow">
              {auth ? 
                  <Link to='/' onClick={handleLogout}>Logout</Link>
                : 
                  <><Margin>
                    <Link to='/signup'>Signup</Link>
                  </Margin>
                  <Link to='/login'>Login</Link></>
              } 
            </Nav>
          </div>
    </Header>
  );
});
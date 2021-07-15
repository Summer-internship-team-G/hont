import React from 'react';
import { Link } from 'react-router-dom';
import styled from "styled-components";


const Logo = styled.li`
    color: #FFFFFF;
    font-size: 130px;
    font-weight: 600;
    font-family: "Baloo Bhaijaan", sans-serif;
    list-style: none;
    /* box-shadow: 4px 4px 4px 0px rgba(0, 0, 0, 0.25); */
`;

const Head = styled.header`
  position: relative;
  top: 30px;
  left: 150px;
`;

export default () => {
  return (
    <Head>
      <Logo><Link to='/'>HONT</Link></Logo>
    </Head>
  )
}
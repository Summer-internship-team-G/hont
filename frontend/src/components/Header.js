import React from 'react';
import { Link } from 'react-router-dom';

export default () => {
  return (
    <header>
      <span><Link to='/'>HONT</Link></span>
      <Link to='/login'>Login</Link>
    </header>
  )
}
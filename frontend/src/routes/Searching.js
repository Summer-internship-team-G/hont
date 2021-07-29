import React, { Component } from 'react';
import SearchForm from '../components/SearchForm';
import styled from 'styled-components';

const DForm = styled.div`
 
margin-left: 40rem;
margin-top: 5rem;
 
`;


class Searching extends Component {
  render() {
    return (

      <div className="App">
        
   
        <SearchForm />
        
      </div>
    );
  }
}
export default Searching;
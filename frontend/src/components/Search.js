import React, { useState } from "react";
import { Link, useLocation } from 'react-router-dom';
import styled, {css} from "styled-components";

const FormData = styled.div(
    css`
   
    height: 50px;
    width: 400px;
    margin-top: 140px;
    margin-left: 600px;
    text-align: center;
    font-size: 18px;
    display: inline-block;
    `
    );




const DEFAULT_PALECEHOLDER_IMAGE = "";

const Search = (props) =>{

const [searchValue, setSearchValue] = useState("");

const handleSearchInputChanges = (e) =>{
    setSearchValue(e.target.value);
}
const resetInputField = ()=> {
    setSearchValue("")
}
const callSearchFunction = (e) => {
    e.preventDefault();
    console.log(searchValue);
    props.search(searchValue);
    resetInputField();
}

    return (
    <FormData>
      <form className="search">
          <input
            value={searchValue}
            onChange={handleSearchInputChanges}
            type="text"/>
            <input onclick={callSearchFunction} type="submit" value="SEARCH"/>
      </form>
      </FormData>
    );
};
export default Search;

import React from "react";
import axios from "axios";

export default () => {
    const getUrl = "http://localhost:5000/user/checkLogin";
    
    const getData = async () => {
        await axios.get(getUrl)
        .then((response) => {
            if(response.data.error == "true"){
                console.log("세션 없음");
                return false;
            }
            else{
                return true;
            }
        })
    }

    return(
        <>
            {getData()}
        </>
    );
}
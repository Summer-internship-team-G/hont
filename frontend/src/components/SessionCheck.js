import React from "react";
import axios from "axios";

export default () => {
    // const [ exist, setExist ] = useState(false);
    const getUrl = "http://localhost:5000/auth/status";
    
    const getData = async () => {
        await axios.get(getUrl)
        .then((response) => {
            if(response.data.error == "true"){
                console.log("세션 없음");
                return false;
            }
            else if(response.data.error == "false"){
                return true;
            }
            return false;
        })
    }

    return(
        <>
            {getData()}
        </>
    );
}
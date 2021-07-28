import React from "react";

const DEFAULT_PALECEHOLDER_IMAGE = "";

const Detail = ({detail}) =>{

const photos = 
    detail.photos === "N/A" ? DEFAULT_PALECEHOLDER_IMAGE : detail.Photos;

    return (

        <div className = "detail">
            <h2>{detail.Title}</h2>
            <div>
                <img
                    width = "200"
                    alt = {'운동 명: {detail.Title}'}
                    src={photos}/>

            </div>
                <p>({detail.tool})</p>
        </div>




    );

};
export default Detail;

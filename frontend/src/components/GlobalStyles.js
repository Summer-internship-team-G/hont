import { createGlobalStyle } from "styled-components";
import reset from "styled-reset";

const GlobalStyles = createGlobalStyle`
    ${reset}

    * {
        box-sizing: border-box;
    }

    html {
        /* min-height: 100%; */
    }

    body {
        /* min-height: 100%; */
        /* position: relative; */
        /* background-color: #000000; */
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        font-size: 16px;
        color: #FFF;
    }

    a {
        color: inherit;
        font-family: inherit;
        font-size: inherit;
        text-decoration: none;
    }
   
    .contents1{
        text-align: center;
        margin-top: 100px;
    }

    .contents2{
        text-align: center;
        margin-top: 150px;
    }

    .lightest{
        background-color: rgba(5, 128, 217, 0.4);
    }

    .neutral{
        background-color: rgba(5, 128, 217, 0.6);
    }

    .darkest{
        background-color: rgba(5, 128, 217, 0.8);
    }

    .lightYellow{
        background-color: rgba(255, 248, 216, 1);
    }

    .bigBtn{
        margin-top: 200px;
        font-size: 72px;
        width: 420px;
        height: 195px;
        margin-left: 40px;
        margin-right: 40px;
        color: white;
        font-family: "Coda";
        font-weight: bold;
        border-radius: 150px;
        border: 0;
        outline: 0;
    }

    .middleBtn{
        margin-top: 150px;
        height: 100px;
        width: 175px;
        font-weight: 800;
        font-size: 36px;
        color: white;
        font-family: "Coda";
        font-weight: bold;
        border-radius: 150px;
        border: 0;
        outline: 0;
    }

    .smallBtn{
        height: 65px;
        width: 200px;
        font-weight: 800;
        font-size: 24px;
        color: black;
        font-family: "Coda";
        font-weight: bold;
        border-radius: 30px;
        border: 0;
        outline: 0;
        margin-left: 20px;
        margin-right: 20px;
    }

`;

export default GlobalStyles;
import { createGlobalStyle } from "styled-components";
import reset from "styled-reset";

const GlobalStyles = createGlobalStyle`
    ${reset}

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        font-family: "Noto Sans KR", sans-serif;
        font-size: 16px;
        color: #FFF;
    }
    
    a {
        color: inherit;
        font-family: inherit;
        font-size: inherit;
        text-decoration: none;
    }

    .boxShadow{
        box-shadow: 0px 5px 20px -5px #606060;
    }

    .textShadow{
        text-shadow: 3px 3px 5px #606060;
    }

    /* small */
    .contents2{
        min-height: calc(100vh - 400px);
        text-align: center;
        margin-top: 80px;
        margin-bottom: 80px;
    }

    .hontLogo{
        -webkit-filter: drop-shadow(3px 3px 3px gray) invert(100%) sepia(0%) saturate(2%) hue-rotate(241deg) brightness(103%) contrast(101%);
        filter: drop-shadow(4px 4px 2px #8F8F8F) invert(100%) sepia(0%) saturate(2%) hue-rotate(241deg) brightness(103%) contrast(101%);
        height: 90px;
        width: 100px;
    }

    .headerContainer{
        width: 100%;
        display: flex;
        flex-flow: row wrap;
        justify-content: space-between;
        align-items: center;
    }

    .headerItem{
        flex-grow: 0;
    }

    .headerItem:nth-child(1){
        flex-shrink: 0;
        flex-basis: 600px;
    }

    .headerItem:nth-child(2){
        flex-grow: 1;
    }

     /* IE10+ */
    @media screen and (-ms-high-contrast: active), (-ms-high-contrast: none) {
        .contents2Container, .guideLineContainer{
            width: 100%;
            display: flex;
            flex-flow: row wrap;
            justify-content: space-around;
            align-items: center;
            align-content: space-around;
        }
    }
    .contents2Container{
        width: 100%;
        display: flex;
        flex-flow: row wrap;
        justify-content: space-evenly;
        align-items: center;
        align-content: space-around;
    }

    .contents2Item:nth-child(1){
        flex-basis: 900px;
    }

    .contents2Item:nth-child(2){
        flex-basis: 500px;
    }

    .contents2Item:nth-child(3){
        flex-basis: 100%;
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
        box-shadow: 0px 5px 20px -5px #606060;
    }

    .bigBtn{
        margin-top: 100px;
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
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
`;

export default GlobalStyles;
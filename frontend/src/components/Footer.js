import styled from "styled-components";

const Footer = styled.footer`
    padding-top: 5px;
    z-index: 20;
    width: 100%;
    height: 80px;
    text-align: center;
    position: relative;
    bottom: 0;
    padding-top: 20px;
`;

const Div = styled.div`
    color: black;
    font-weight: 400;
`;


export default () => {
    return (
        <Footer>
            <Div>권예진 류건열 김시정 장민지 최예은</Div>
            <Div>SiliconValley Online Internship</Div>
            <Div>ZoomMate Team. All rights reserved.</Div>
        </Footer>
    )
}

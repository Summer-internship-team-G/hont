import styled from "styled-components";

const Footer = styled.footer`
    z-index: 20;
    position: fixed;
    bottom: 0;
	left: 0;
	right: 0;
    width: 100%;
    height: 60px;
    text-align: center;
`;

const Div = styled.div`
    color: black;
    /* margin-bottom: 5px; */
`;


export default () => {
    return (
        <Footer>
            <Div>권예진 류건열 김시정 장민지 최예은</Div>
            <Div>SilliconValley Online Internship</Div>
            <Div>ZoomMate Team. All rights reserved.</Div>
        </Footer>
    )
}
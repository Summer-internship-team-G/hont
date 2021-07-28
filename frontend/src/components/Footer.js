import styled from "styled-components";

const Footer = styled.footer`
    padding-top: 5px;
    z-index: 20;
    width: 100%;
    height: 80px;
    text-align: center;
    /* background-color: #d8d8d8; */
    position: relative;
    bottom: 0;
    padding-top: 20px;
    /* display : flex;
    align-items: center;
    justify-content: center; */
`;

const Div = styled.div`
    color: black;
    font-weight: 400;
    /* font-family: "Baloo Bhaijaan", sans-serif; */
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
import React, { useState, useEffect }  from 'react';
import styled from "styled-components";

const Background = styled.div`
    position: absolute;
    top: 0; left: 0;
    z-index: -10;
`;

const SVG1 = () => {
    const [width, setWidth] = useState(document.body.offsetWidth);
    const halfWidth = width / 2;
    const left = (width - halfWidth) / 2;
    const right = (width + halfWidth) / 2;

    const handleResize = () => {
        setWidth(document.body.offsetWidth);
    }

    useEffect(() => {
        window.addEventListener("resize", handleResize);

        return () => {
        window.removeEventListener("resize", handleResize);
        }
    });

    return (
        // <header>
            <Background>
                <svg width={width} height="200" viewBox={`0 0 ${width} 200`} fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d={`M${halfWidth} 200 C${left} 200 0 160 0 160 V 0 H ${width} V 160 C ${width} 160 ${right} 200 ${halfWidth} 200Z`} fill="url(#paint0_linear)"/>
                    <defs>
                    <linearGradient id="paint0_linear" x1={right} y1="0" x2={halfWidth} y2="500" gradientUnits="userSpaceOnUse">
                        <stop stopColor="#12D3CF"/>
                        <stop offset="1" stopColor="#B0F4E6"/>
                    </linearGradient> 
                    </defs>
                </svg>
            </Background>
        // </header>
    )
}
const SVG2 = () => {
    const [width, setWidth] = useState(document.body.offsetWidth);
    const halfWidth = width / 2;
    const left = (width - halfWidth) / 2;
    const right = (width + halfWidth) / 2;

    const handleResize = () => {
        setWidth(document.body.offsetWidth);
    }

    useEffect(() => {
        window.addEventListener("resize", handleResize);

        return () => {
        window.removeEventListener("resize", handleResize);
        }
    });

    return (
            <Background>
                <svg width={width} height="1000" viewBox={`0 0 ${width} 1000`} fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d={`M${halfWidth} 1000 C${left} 1000 0 800 0 800 V 0 H ${width} V 800 C ${width} 800 ${right} 1000 ${halfWidth} 1000Z`} fill="url(#paint0_linear)"/>
                    <defs>
                    <linearGradient id="paint0_linear" x1={right} y1="0" x2={halfWidth} y2="800" gradientUnits="userSpaceOnUse">
                        <stop stopColor="#12D3CF"/>
                        <stop offset="1" stopColor="#B0F4E6"/>
                    </linearGradient> 
                    </defs>
                </svg>
            </Background>
    )
}

export default{
    SVG1,
    SVG2,
}    
import React from "react";
import { Link, useLocation } from 'react-router-dom';
import styled from "styled-components";

const ExerciseResult = styled.div`
    height: 350px;
    width: 600px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 30px;
    border-radius: 0px;
`;

const Content = styled.div`
    position: relative;
    top: 105px;
`;

const P = styled.p`
    font-size: 64px;
    font-weight: 800;
`;

const Date = styled.span`
    font-size: 48px;
    font-weight: 800;
`;

const Result = () => {
    const location = useLocation();
    const date = location.state.date;
    const time = location.state.time;
    const count = location.state.count;

    return (
        <>
            <div className="contents1">
                <Date className="textShadow2">
                    {date}
                </Date>
                <ExerciseResult className="lightest boxShadow">
                    <Content>
                        <P>
                            운동 시간 : {time}초
                        </P>
                        <P>
                            총 횟수 : {count}회
                        </P>
                    </Content>
                </ExerciseResult>
                <Link to='/'><button className="neutral middleBtn boxShadow">돌아가기</button></Link>
            </div>
        </>
    ) 
}

export default Result;
import React from "react";
import { Link } from 'react-router-dom';
import pushup from '../images/pushup.png';
import squat from '../images/squat.png';
import styled from "styled-components";

export default ({num, link}) => {
    const PushupConditionBox = styled.div`
        height: 630px;
    `;

    const SquatConditionBox = styled.div`
        height: 500px;
    `;

    const Guide = styled.div`
        text-align: left !important;
        flex-basis: 100%;
        margin-top: 15px;
        margin-bottom: 15px;
    `;

    return(
        <div className="contents2 guideLineContainer">
            <div className="guideLineItem">
                {num == 1 ? // 1 == 스쿼트
                    <img src={squat} className="squatImg boxShadow"/>
                : // 2 == 푸시업
                    <img src={pushup} className="pushupImg boxShadow"/>   
                }
            </div>
                {num == 1 ? // 1 == 스쿼트
                    <SquatConditionBox className="guideLineItem lightYellow">
                        <Guide>
                            <div>조건 1. 엉덩이 각도( 무릎-엉덩이-어깨 )가 60도~140도 사이</div>
                            <div>조건 2. 허벅지가 바닥과 수평</div>
                            <div>조건 3. 무릎과 발끝 선 일치</div>
                        </Guide>
                        <Guide>
                            <div>-> 조건 1, 2, 3을 모두 만족시킬 때 바른자세로 인식하여 스쿼트 횟수를 증가시키고, 정해진 조건에서 벗어나게 되면 가이드라인이 맞춰나오게 됩니다.</div>
                        </Guide>
                    </SquatConditionBox>
                : // 2 == 푸시업
                    <PushupConditionBox className="guideLineItem lightYellow">
                        <Guide>
                            <div>조건 1. 팔꿈치 각도 ( 팔목-팔꿈치-어깨 ) 가 70도~100도 사이</div>
                            <div>조건 2. 바디 각도( 어깨-엉덩이-발목 )가 160도~200도 사이</div>
                        </Guide>
                        <Guide>
                            <div>-> 조건1, 2를 모두 만족시킬 때 바른자세로 인식하여 푸시업  횟수를 증가시키고, 정해진 각도에서 틀어지게 되면 가이드라인이 맞춰나오게 됩니다.</div>
                        </Guide>
                    </PushupConditionBox>
                }
            <div className="guideLineItem">
                <Link to='/'><button className="lightYellow smallBtn">돌아가기</button></Link>
                <Link to={link}><button className="lightYellow smallBtn">시작하기</button></Link>
            </div>
        </div>
    )
};
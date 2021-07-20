import React from "react";
import { Link } from "react-router-dom";
import Session from '../components/SessionCheck';

export default () => {
    const noSession = () => {
        alert("로그인이 필요합니다.");
    }
    return(
        <div className="contents1">
            {<Session/> ? 
                    <>
                        <Link to='/pushup/guideLine'><button className="lightest bigBtn">푸시업</button></Link>
                        <Link to='/squat/guideLine'><button className="neutral bigBtn">스쿼트</button></Link>
                        <Link to='/statistics'><button className="darkest bigBtn">통계</button></Link>
                    </>
                :
                    <>
                        <button className="lightest bigBtn" onClick={noSession}>푸시업</button>
                        <button className="neutral bigBtn" onClick={noSession}>스쿼트</button>
                        <button className="darkest bigBtn" onClick={noSession}>통계</button>
                    </>
            }
        </div>
    )
};
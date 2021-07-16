import React from "react";
import { Link } from 'react-router-dom';

export default ({link}) => (
    <>
        <div className="contents2">
            {/* 가이드라인 이미지 */}
            <Link to='/'><button className="lightYellow smallBtn">돌아가기</button></Link>
            <Link to={link}><button className="lightYellow smallBtn">시작하기</button></Link>
        </div>
    </>
);
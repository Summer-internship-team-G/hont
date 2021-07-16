import React from "react";
import { Link } from "react-router-dom";

export default () => (
    <>
        <div className="contents1">
            <Link to='/pushup/guideLine'><button className="lightest bigBtn">푸시업</button></Link>
            <Link to='/squat/guideLine'><button className="neutral bigBtn">스쿼트</button></Link>
            <Link to='./statistics'><button className="darkest bigBtn">통계</button></Link>
        </div>
    </>
);
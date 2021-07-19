import React from "react";
import { Link, useLocation } from 'react-router-dom';

const Result = () => {
    const location = useLocation();
    // console.log(location);
    const date = location.state.date;
    const time = location.state.time;
    const count = location.state.count;

    return (
        <>
            <div className="contents1">
                <span>
                    {date}
                </span>
                <div className="lightest">
                    <div>
                        <p>
                            운동 시간 : {time}초
                        </p>
                        <p>
                            총 횟수 : {count}회
                        </p>
                    </div>
                </div>
                <Link to='/'><button className="neutral middleBtn">돌아가기</button></Link>
            </div>
        </>
    ) 
}

export default Result;
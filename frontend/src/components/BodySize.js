import React from "react";
import { Link } from 'react-router-dom';


// function showButton(){
//     setTimeout(() => {
//         document.getElementsByClassName("next_btn").style.display = "block";
//     }, 10000);
// }

export default ({text, link}) => (
    <div>
        <h3>{text} 바디 사이즈</h3>
        {/* 영상 */}
        {/* <button onClick={this.showButton()}>시작하기</button> */}
        <button>사이즈 측정하기</button>
        {/* 시작하기 버튼 누르고 몇초 뒤 다음 버튼 생기게 */}
        {/* <button className="next_btn" style="display=hidden">다음</button> */}
        <button>다음</button>
        <Link to={link}><button>운동 시작하기</button></Link>
    </div>
);
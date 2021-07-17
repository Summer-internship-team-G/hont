import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";
import Webcam from "react-webcam";

//  start   stop
//  false   false (초기)
// --------------------------
//  true    false (운동start)
//  false   true  (운동stop)

// function Dosquat({ num, id }) {
function Exercise({ num }) {
    const useGetData = () => {
        const webcamRef = useRef(null);
        const [start, setStart] = useState(false);
        const [stop, setStop] = useState(false);
        const [time, setTime] = useState(-1);
        const [ImgSrc, setImgSrc] = useState(null);

        const clickStartBtn = (e) => {
            e.preventDefault();
            setStart(true);
        };

        useEffect(() => {
            const countUp = setInterval(() => {
                if(start){
                    setTime(parseInt(time) + 1);
                    const imageSrc = webcamRef.current.getScreenshot();
                    setImgSrc(imageSrc);
                }
            }, 1000);
            return () => clearInterval(countUp);
        }, [time, start]);

        const postInfo = async () => {
        }

        const clickStopBtn = (e) => {
            e.preventDefault();
            setStop(true);
            setStart(false);
        }

        return {
            start,
            stop,
            clickStartBtn,
            clickStopBtn,
            webcamRef,
            time,
            ImgSrc,
        };
    };
    
    const postUrl = "http://localhost:5000/api/upload";
    const history = useHistory();
    const { start, stop, clickStartBtn, clickStopBtn, webcamRef, time, ImgSrc } = useGetData();
    const videoConstraints = {
        width: 700,
        height: 500,
        facingMode: "user",
    };
    
    //버튼 눌렀을 때 axios 써서 값 받아오기
    const clickQuitBtn = (e) => {
        e.preventDefault();
        let today = new Date();
        today = today.toLocaleDateString();
        history.push({
            pathname: "/components/Result",
            state: { 
                date: today,
                time: 1, 
                count: 2, 
            }
            // state: { 
            //     date: today, 
            //     time: time, 
            // }
        })
    }

    useEffect(() => {
        fetch(ImgSrc)
        .then(res => res.blob())
        .then(blob => {
            const file = new File([blob], "img", {type: "image/jpeg"});
            // console.log(file);
            postData(file);
        });
    // },[ImgSrc, time]);
    },[ImgSrc]);

    const postData = async (file) => {
        const postVal = { 
            type: {num}, 
            image: {file},
        }
        await axios.post(postUrl, postVal);
    }

    return start || stop ? (
        <>
            <div className="contents2">
                <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    videoConstraints={videoConstraints}
                />
                <div className="lightYellow">
                    <div>
                        <p>
                            가이드라인 : guideLine
                        </p>
                        <p>
                            시간 : {time}
                        </p>
                        <p>
                            횟수 : count
                        </p>
                    </div>
                </div>
                <button id="stopBtn" className="lightYellow smallBtn" disabled={stop} onClick={clickStopBtn}>그만하기</button>
                <button id="quitBtn" className="lightYellow smallBtn" disabled={!stop} onClick={clickQuitBtn}>종료하기</button>
            </div>
        </>
    ) : (
        <>
            <div className="contents2">
                <button className="lightYellow smallBtn" onClick={clickStartBtn}>운동시작</button>
            </div>
        </>
    );
}

export default Exercise;
import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";
import Webcam from "react-webcam";
import styled from "styled-components";

//  start   stop
//  false   false (초기)
// --------------------------
//  true    false (운동start)
//  false   true  (운동stop)

const PresentResult = styled.div`
    height: 500px;
    margin-top: 50px;
    margin-bottom: 50px;
    display: flex;
    align-items: center;
    align-content: center;
    flex-flow: row wrap;
`;

const ExerInfo = styled.div`
    flex-basis: 100%;
    color: black;
    font-size: 36px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 10px;
`;

function Dosquat({ num }) {
    const useGetData = () => {
        const webcamRef = useRef(null);
        const [start, setStart] = useState(false);
        const [stop, setStop] = useState(false);
        const [time, setTime] = useState(-1);
        const [ImgSrc, setImgSrc] = useState(null);
        const [guideLine, setGuideLine] = useState("");
        const [count, setCount] = useState(0);
        
        const clickStartBtn = (e) => {
            e.preventDefault();
            setStart(true);
        };

        //1초마다 time 증가, frame 변경
        useEffect(() => {
            const countUp = setInterval(() => {
                if(start){
                    setTime(parseInt(time) + 1);
                    const imageSrc = webcamRef.current.getScreenshot();
                    setImgSrc(imageSrc);
                    // console.log(imageSrc);
                }
            }, 1000);
            return () => clearInterval(countUp);
        }, [time, start]);

        //image를 Blob file로 변환
        const dataURItoBlob = (dataURI) => {
            if(dataURI != null){
            let byteString = atob(dataURI.split(",")[1]);
            let mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];        
            let ab = new ArrayBuffer(byteString.length);
            let ia = new Uint8Array(ab);
            for (let i = 0; i < byteString.length; i++) {
              ia[i] = byteString.charCodeAt(i);
            }
            
            return new Blob([ab], { type: mimeString });}
          };
    
        //Image를 file로 변환하여 post
        useEffect(() => {
            const info = new FormData();
            //info.append('type', num);
            const file = dataURItoBlob(ImgSrc);
            info.append('file', file);
            postData(info);
        },[ImgSrc]);
    
        //file로 변환된 image를 post하고, 돌아오는 값으로 guideLine과 count setting
        const postData = async (info) => {
            //num == 1 : squat / num == 2 : pushup
            let target = "";
            num == 1 ? target = "analyzeSquat" : target = "analyzePushup";
    
            await axios.post("http://localhost:5000/api/" + target, info).then((response) => {
                if (response.data) {
                    setGuideLine(response.data.guide);
                    setCount(count + response.data.count);
                }
                else {
                    console.log('response 실패');
                }
            });
        }

        //stop 버튼을 눌렀을 때 database에 저장하기 위한 post
        const postInfo = async () => {
            let today = new Date();
            today = today.toLocaleDateString();
            const postVal = {
                id: localStorage.getItem('id'),
                exerDate: today,
                exerType: num,
                exerNum: count,
                exerTime: time,
            }
            await axios.post("http://localhost:5000/recordex", postVal);
        }

        //stop 버튼 핸들러
        const clickStopBtn = (e) => {
            e.preventDefault();
            setStop(true);
            setStart(false);
            postInfo();
        }

        return {
            start,
            stop,
            clickStartBtn,
            clickStopBtn,
            webcamRef,
            time,
            ImgSrc,
            guideLine,
            count,
        };
    };
    
    const history = useHistory();
    const { start, stop, clickStartBtn, clickStopBtn, webcamRef, time, guideLine, count } = useGetData();
    const videoConstraints = {
        width: 900,
        height: 500,
        facingMode: "user",
    };
    
    //버튼 눌렀을 때 axios 써서 값 받아오기
    const clickQuitBtn = (e) => {
        e.preventDefault();
        let newDate = new Date();
        let date = newDate.getDate();
        let month = newDate.getMonth() + 1;
        let year = newDate.getFullYear();

        let today = `${year}년 ${month}월 ${date}일`;
        history.push({
            pathname: "/Result",
            state: { 
                date: today, 
                time: time, 
                count: count, 
            }
        })
    }

    return start || stop ? (
        <>
            <div className="contents2 contents2Container">
                <div className="contents2Item boxShadow">
                    <Webcam
                        audio={false}
                        ref={webcamRef}
                        screenshotFormat="image/jpeg"
                        videoConstraints={videoConstraints}
                    />
                </div>
                <PresentResult className="lightYellow contents2Item">
                        <ExerInfo>
                            시간 : {time} {" "}
                            횟수 : {count}
                        </ExerInfo>
                        <ExerInfo>
                            가이드라인 : {guideLine}
                        </ExerInfo>
                </PresentResult>
                <div className="contents2Item">
                    <button id="stopBtn" className="lightYellow smallBtn" disabled={stop} onClick={clickStopBtn}>그만하기</button>
                    <button id="quitBtn" className="lightYellow smallBtn" disabled={!stop} onClick={clickQuitBtn}>종료하기</button>
                </div>
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

export default Dosquat;
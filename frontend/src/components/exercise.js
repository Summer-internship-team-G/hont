import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";
import SVG from "../components/SVG";
import Webcam from "react-webcam";
import styled from "styled-components";

//  start   stop
//  false   false (초기)
// --------------------------
//  true    false (운동start)
//  false   true  (운동stop)

const PresentResult = styled.div`
    height: 200px;
    width: 700px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 50px;
    margin-bottom: 50px;
    /* left: 80%; */
`;

const Content = styled.div`
    position: relative;
    top: 50px;
`;

const P = styled.p`
    color: black;
    font-family: "Coda";
    font-size: 36px;
    font-weight: 600;
`;

// function Dosquat({ num, id }) {
function Dosquat({ num }) {
    const useGetData = () => {
        const webcamRef = useRef(null);
        const [start, setStart] = useState(false);
        const [stop, setStop] = useState(false);
        const [time, setTime] = useState(-1);
        const [ImgSrc, setImgSrc] = useState(null);
        const [guideLine, setGuideLine] = useState("");
        const [count, setCount] = useState(0);
        const dataURItoBlob = (dataURI) => {
            let byteString = atob(dataURI.split(",")[1]);
            let mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
        
            let ab = new ArrayBuffer(byteString.length);
            let ia = new Uint8Array(ab);
            for (let i = 0; i < byteString.length; i++) {
              ia[i] = byteString.charCodeAt(i);
            }
        
            return new Blob([ab], { type: mimeString });
          };
        
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
                    // console.log(imageSrc);
                }
            }, 1000);
            return () => clearInterval(countUp);
        }, [time, start]);

        // 마지막 언마운트시 ? count??
        useEffect(() => {
            const getData = setInterval(() => {
                
                if(start){
                    axios.get(getUrl)
                    .then(({ count, guideLine }) => {
                        setGuideLine(guideLine);
                        console.log(guideLine);
                        setCount(count);
                    })
                    .catch(e => {
                        console.error(e);
                    });
                }
            }, 5000);
            return () => clearInterval(getData);
        }, [time, start])

        const postInfo = async () => {
            let today = new Date();
            today = today.toLocaleDateString();
            const postVal = {
                // id: {id},
                exerDate: {today},
                exerType: {num},
                exerNum: count,
                exerTime: time,
            }
            await axios.post(postUrl, postVal);
        }

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
    
    const postUrl = "http://localhost:5000/api/upload";
    const getUrl = "/api/upload";
    const history = useHistory();
    const { start, stop, clickStartBtn, clickStopBtn, webcamRef, time, ImgSrc, guideLine, count } = useGetData();
    const [guide, setGuideLine] = useState("");
    const [counte, setCount] = useState(0);
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
            // search: true,
            state: { 
                date: today,
                time: 1, 
                count: 2, 
            }
            // state: { 
            //     date: today, 
            //     time: {time}, 
            //     count: {count}, 
            // }
        })
    }

    useEffect(() => {
        fetch(ImgSrc)
        
            // const file = new File([blob], "img", {type: "image/jpeg"});
            // //console.log(file);
            
            // postData(file);
            const dataURItoBlob = (dataURI) => {
                if(dataURI!=null){
                let byteString = atob(dataURI.split(",")[1]);
                let mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
            
                let ab = new ArrayBuffer(byteString.length);
                let ia = new Uint8Array(ab);
                for (let i = 0; i < byteString.length; i++) {
                  ia[i] = byteString.charCodeAt(i);
                }
                
                return new Blob([ab], { type: mimeString });}
              };
            
            const info = new FormData();
            //info.append('type', num);
            const file = dataURItoBlob(ImgSrc);
            info.append('file', file);
            postData(info);

    // },[ImgSrc, time]);
    },[ImgSrc]);

    const postData = async (info) => {
        // const postVal = { 
        //     type: {num}, 
        //     image: "dd",
        // }
       // await axios.post(postUrl, info);
       
       setGuideLine("");
       var before_count = counte
    
        axios.post("http://localhost:5000/api/upload", info).then((response) => {
      if (response.data) {
          console.log(response.data);
          console.log(response.data.count);
          console.log(response.data.guide);
          
          setGuideLine(response.data.guide);
          setCount(counte + response.data.count);
       
      } else {
        console.log('response 실패');
      }
    });
    }

    // const getData = async () => {
    //     axios.get(getUrl)
    //     .then(({ file, count }) => {
    //         // set
    //     })
    //     .catch(e => {
    //         console.error(e);
    //     });
    // }

    return start || stop ? (
        <>
            <SVG.SVG1/>
            <div className="contents2">
                <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    videoConstraints={videoConstraints}
                />
                <PresentResult className="lightYellow">
                    <Content>
                        <P>
                            가이드라인 : {guide}
                        </P>
                        <P>
                            시간 : {time}
                        </P>
                        <P>
                            횟수 : {counte}
                        </P>
                    </Content>
                </PresentResult>
                <button id="stopBtn" className="lightYellow smallBtn" disabled={stop} onClick={clickStopBtn}>그만하기</button>
                <button id="quitBtn" className="lightYellow smallBtn" disabled={!stop} onClick={clickQuitBtn}>종료하기</button>
            </div>
        </>
    ) : (
        <>
            <SVG.SVG1/>
            <div className="contents2">
                <button className="lightYellow smallBtn" onClick={clickStartBtn}>운동시작</button>
            </div>
        </>
    );
}

export default Dosquat;
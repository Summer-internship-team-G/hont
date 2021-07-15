import React, { useState, useRef, useEffect, useCallback } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";
import SVG from "../components/SVG";
import Webcam from "react-webcam";
import ReactWebCamCapture from 'react-webcam-capture';

function Dosquat({ num }) {
    const useGetData = () => {
        const webcamRef = useRef(null);
        const [start, setStart] = useState(false);
        const [stopTime, setStopTime] = useState(null);
        const [screenShot, setScreenShot] = useState(null);
        const [minutes, setMinutes] = useState(0);
        const [seconds, setSeconds] = useState(0);

        // const postUrl = "/hont";
        // const transfer = async (startTime) => {
        //     const postVal = { kinds: {num}, time: {startTime}, screenShot: {screenShot} };
        //     await axios.post(postUrl, postVal);
        // }

        const clickStartBtn = (e) => {
            // let today = new Date();
            // let startTime = today.toLocaleTimeString();
            e.preventDefault();
            setStart(true);
            // useEffect(() => {
            //     if (!stop) {
            //         setScreenShot(this.webcam.getScreenshot());
            //         const postVal = { kinds: {num}, time: {startTime}, screenShot: {screenShot} };
            //         await axios.post(postUrl, postVal);
            //     }
            // }, [screenShot]);
            // transfer(today.toLocaleTimeString());
        };

        const handleUserMedia = () => {
            setTimeout(() => {
              const imageSrc = webcamRef.current.getScreenshot();
              console.log(imageSrc);
            //   setImgSrc(imageSrc);
            }, 1000);
          };
        

        useEffect(() => {
            const countUp = setInterval(() => {
                setSeconds(parseInt(seconds) + 1);
                if(parseInt(seconds) === 59){
                    setMinutes(parseInt(minutes) + 1);
                    setSeconds(0);
                }
            }, 1000);
            return () => clearInterval(countUp);
        }, [minutes, seconds]);


        //     console.log(1111);
        //     if(webcamRef.current){
        //         const { current } = webcamRef;
        //         console.log(current);
        //         const imageSrc = current.getScreenshot();
        //         setScreenShot(imageSrc);
        //         console.log(screenShot);
        //     }
        // },[screenShot, start]);

        const clickStopBtn = (e) => {
            let today = new Date();
            setStopTime(today.toLocaleTimeString());
            e.preventDefault();
            setStart(false);
        }

        return {
            start,
            clickStartBtn,
            clickStopBtn,
            stopTime,
            screenShot,
            webcamRef,
            handleUserMedia,
            minutes,
            seconds,
        };
    };


    const getInfo = async (stopTime) => {
        const getUrl = "/hont";
        const getVal = { time: {stopTime} }
        // axios.get(getUrl, {
        //     params: getVal
        // })
        // .then(function (resposnse){
            
        // })
        return await axios.get(getUrl, {
            param: getVal
        })
    }

    //버튼 눌렀을 때 axios 써서 값 받아오기
    const clickQuitBtn = (e) => {
        e.preventDefault();
        // data = getInfo(stopTime);
        history.push({
            pathname: "/compoenet/Result",
        //     state: { count: data.count, time: data.time }
        })
    }

    const history = useHistory();
    const { start, clickStartBtn, clickStopBtn, stopTime, screenShot, webcamRef, handleUserMedia, minutes, seconds } = useGetData();
    const videoConstraints = {
        width: 600,
        height: 400,
        facingMode: "user"
    };
    
    useEffect(() => {
        if(start){
            console.log(screenShot);
        }
    })
    console.log(screenShot);

    return start ? (
        <>
            <SVG.SVG1/>
            <div className="contents2">
                <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    videoConstraints={videoConstraints}
                    onUserMedia={handleUserMedia}
                />
                <h2>
                    {minutes}:{seconds < 10 ? `0${seconds}` : seconds}
                </h2>
                <button id="stopBtn" disabled={!start} onClick={clickStopBtn}>그만하기</button>
                <button id="quitBtn" disabled={start} onClick={clickQuitBtn}>종료하기</button>
            </div>
        </>
    ) : (
        <>
            <SVG.SVG1/>
            <div className="contents2">
                <button onClick={clickStartBtn}>운동시작</button>
            </div>
        </>
    );
}

// const videoConstraints = {
//     width: 400,
//     height: 400,
//     facingMode: "user"
//   };
  
//   const Dosquat = () => {
//       const webcamRef = React.useRef();
//       useEffect(() => {
//             const imageSrc = webcamRef.current.getScreenshot();
//             console.log(imageSrc);
//         }, [webcamRef]);
    
    
//     // console.log(webcamRef.current.getScreenshot());

//     // const Capture = () => {
//     //     useEffect(() => {
//     //         const imageSrc = webcamRef.current.getScreenshot();
//     //         console.log(imageSrc);
//     //     }, [webcamRef]);
//     // }
//     // const capture = React.useCallback(
//     //   () => {
//     //     const imageSrc = webcamRef.current.getScreenshot();
//     //     console.log(imageSrc);
//     //   },
//     //   [webcamRef]
//     // );
  
//     return (
//       <>
//         <Webcam
//           audio={false}
//           ref={webcamRef}
//           screenshotFormat="image/jpeg"
//           videoConstraints={videoConstraints}
//         />
//         {/* <button onClick={Capture}>Capture photo</button> */}
//       </>
//     );
//   };

export default Dosquat;